import pytest
import json
import os
from openindexmaps_py.metadata import GeoBlacklight_Metadata  # replace 'your_module' with the actual module name where GeoBlacklight_Metadata is defined

# Helper function to load a JSON file
def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def test_default_metadata():
    metadata = GeoBlacklight_Metadata()
    assert metadata.metadata['id'] == ""
    assert metadata.metadata['dct_title_s'] == ""
    assert metadata.metadata['gbl_resourceClass_sm'] == []
    assert metadata.metadata['dct_accessRights_s'] == ""
    assert metadata.metadata['gbl_mdVersion_s'] == "Aardvark"

def test_set_valid_attribute():
    metadata = GeoBlacklight_Metadata()
    metadata.set_attribute('id', '12345')
    metadata.set_attribute('dct_title_s', 'Example Title')
    metadata.set_attribute('gbl_resourceClass_sm', ['Datasets'])
    metadata.set_attribute('dct_accessRights_s', 'Public')
    
    assert metadata.metadata['id'] == '12345'
    assert metadata.metadata['dct_title_s'] == 'Example Title'
    assert metadata.metadata['gbl_resourceClass_sm'] == ['Datasets']
    assert metadata.metadata['dct_accessRights_s'] == 'Public'

def test_set_invalid_attribute():
    metadata = GeoBlacklight_Metadata()
    with pytest.raises(KeyError):
        metadata.set_attribute('invalid_attribute', 'value')

def test_validate_metadata():
    metadata = GeoBlacklight_Metadata()
    metadata.set_attribute('id', '12345')
    metadata.set_attribute('dct_title_s', 'Example Title')
    metadata.set_attribute('gbl_resourceClass_sm', ['Datasets'])
    metadata.set_attribute('dct_accessRights_s', 'Public')
    
    metadata.validate_metadata()

def test_generate_metadata_file(tmpdir):
    metadata = GeoBlacklight_Metadata()
    metadata.set_attribute('id', '12345')
    metadata.set_attribute('dct_title_s', 'Example Title')
    metadata.set_attribute('gbl_resourceClass_sm', ['Datasets'])
    metadata.set_attribute('dct_accessRights_s', 'Public')
    
    file_path = tmpdir.join('metadata.json')
    metadata.generate_metadata_file(file_path)
    
    generated_metadata = load_json(file_path)
    assert generated_metadata['id'] == '12345'
    assert generated_metadata['dct_title_s'] == 'Example Title'
    assert generated_metadata['gbl_resourceClass_sm'] == ['Datasets']
    assert generated_metadata['dct_accessRights_s'] == 'Public'

if __name__ == '__main__':
    pytest.main()