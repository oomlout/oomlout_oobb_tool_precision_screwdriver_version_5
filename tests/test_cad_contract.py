"""Shared template/plate contract tests; no CAD process is started."""
import copy
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

PROJECT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT))
import working_cad


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CadContractTests(unittest.TestCase):
    def test_populate_declares_type_and_output_flags(self):
        writer=Mock()
        helpers=SimpleNamespace(build_oomp_id=lambda item:'sample',write_extras=writer)
        with patch.dict(sys.modules,{'oomp_populate_helper':helpers,'working_oomp_populate_extra_detail':SimpleNamespace(main=lambda **kwargs:None)}):
            populate=load('population_contract',PROJECT/'working_oomp_populate.py')
            populate.main()
        options=writer.call_args.args[0]
        printable = [part for part in options if 'oobb_details' in part]
        hardware = [part for part in options if 'oobb_details' not in part]
        self.assertEqual(len(hardware), 1)
        self.assertEqual(hardware[0]['id'], 'hardware_screw_countersunk_m3_black_6_mm_length_hex_head')
        archived = {f.parent.name for f in (PROJECT / 'old_version/parts').glob('*/3dpr.scad')}
        for version in ('version_1', 'version_2'):
            records = [part for part in printable if part['taxonomy_2'] == version]
            self.assertEqual(len(records), 38 if version == "version_1" else 40)
            self.assertEqual({part['legacy_id'] for part in records if 'legacy_id' in part}, archived)
            for part in records:
                details = part['oobb_details']
                self.assertEqual(details['oobb_type'], f"{part['oobb_name']}_{version}")
                self.assertIs(details['run_scad'], True)
                self.assertIs(details['run_solidcraft'], False)
                if details['oobb_name'] == 'label_top':
                    self.assertIsInstance(details['siz'], str)

    def test_scad_dispatches_type_instead_of_variant_and_skips_disabled(self):
        selected=Mock(side_effect=RuntimeError('selected type'))
        recipes=SimpleNamespace(get_plate=selected,get_base=Mock(),get_basic=Mock())
        oobb=SimpleNamespace(get_default_thing=lambda **kwargs:{})
        with patch.dict(sys.modules,{'oobb':oobb,'working_scad':recipes}):
            scad=load('scad_contract',PROJECT/'scad_help.py')
        part={'oobb_name':'basic','oobb_details':{'oobb_type':'plate'},'kwargs':{'oobb_type':'plate','run_scad':True,'run_solidcraft':True,'depth':3}}
        with self.assertRaisesRegex(RuntimeError,'selected type'):
            scad.make_scad_generic(part)
        self.assertEqual(selected.call_count,1)
        self.assertNotIn('oobb_type',selected.call_args.kwargs)
        self.assertNotIn('run_scad',selected.call_args.kwargs)
        recipes.get_basic.assert_not_called()
        recipes.get_base.assert_not_called()
        part['oobb_details']['run_scad']=False
        scad.make_scad_generic(part)
        self.assertEqual(selected.call_count,1)

    def test_new_type_needs_only_matching_backend_function(self):
        part={'oobb_name':'basic','oobb_details':{'oobb_type':'bracket'}}
        native=SimpleNamespace(get_bracket=lambda:'native bracket')
        scad=SimpleNamespace(get_bracket=lambda:'scad bracket')
        self.assertEqual(working_cad.resolve_builder(native,part)(),'native bracket')
        self.assertEqual(working_cad.resolve_builder(scad,part)(),'scad bracket')
        with self.assertRaisesRegex(ValueError,'get_bracket'):
            working_cad.resolve_builder(SimpleNamespace(get_base=lambda:None),part,legacy_fallback=True)

    def test_initial_recipes_match_but_are_independently_editable(self):
        def append(thing,**kwargs):
            thing['requests'].append(copy.deepcopy(kwargs))
        with patch.dict(sys.modules,{'oobb':SimpleNamespace(append_full=append), 'oobb_solidcraft':SimpleNamespace(api=SimpleNamespace(append_full=append)), 'scad_help':SimpleNamespace()}):
            scad=load('scad_recipe_contract',PROJECT/'working_scad.py')
            native=load('native_recipe_contract',PROJECT/'working_solidcraft.py')
            for width,height,depth in ((1,1,3),(3,3,3),(3,3,6)):
                a,b={'requests':[]},{'requests':[]}
                scad.get_plate(a,width=width,height=height,depth=depth)
                native.get_plate(b,width=width,height=height,depth=depth)
                self.assertEqual(a,b)
            with patch.object(native,'get_plate',return_value='edited'):
                self.assertEqual(working_cad.resolve_builder(native,{'oobb_details':{'oobb_type':'plate'}})({}),'edited')
                self.assertIsNot(working_cad.resolve_builder(scad,{'oobb_details':{'oobb_type':'plate'}}),native.get_plate)
