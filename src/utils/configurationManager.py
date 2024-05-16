import uuid
import json
import os
from pathlib import Path

def read_json_file(filename):
    current_dir = Path(__file__).parent.parent.parent
    file_path = current_dir / filename
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def write_json_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
def extract_feature_info(model_data, model_id, config_name):
    for product_line in model_data['productLines']:
        for model in product_line['domainEngineering']['models']:
            if model['id'] == model_id:
                configurations = []
                config_id = str(uuid.uuid4())
                config_name = config_name
                features = []
                for element in model['elements']:
                    if element['type'] in ['RootFeature', 'ConcreteFeature', 'AbstractFeature']:
                        feature = {
                            "id": element['id'],
                            "properties": element['properties']  # Assuming we need to set this default
                        }
                        features.append(feature)
                configuration = {
                    "id": config_id,
                    "name": config_name,
                    "features": features
                }
                configurations.append(configuration)
                return {
                    "idModel": model_id,
                    "nameApplication": config_name,
                    "configurations": configurations
                }
def add_configuration_to_json_file(configuration, data):
    data['configurations'].append({
        "id": str(uuid.uuid4()),
        "name": configuration['configurations'][0]['name'],

        "features": configuration['configurations'][0]['features']
    })
    return json.dumps(data, indent=4)


def manage_configurations(model_data, model_id, config_name, data):
    # Generar la información de configuración usando la función existente
    new_config = extract_feature_info(model_data, model_id, config_name)

    # Agregar la nueva configuración al archivo JSON, creando el archivo si no existe
    return add_configuration_to_json_file(new_config, data)

def apply_configuration_to_model(model_json, config_json, config_id):
    # Encontrar la configuración especificada por config_id
    selected_config = None
    for config in config_json['configurations']:
        if config['id'] == config_id:
            selected_config = config
            break

    if not selected_config:
        raise ValueError("Configuration with the specified ID not found")

    # Crear un diccionario de las características con sus valores configurados
    feature_values = {feature['id']: feature['value'] for feature in selected_config['features']}

    # Aplicar los valores configurados a las características en el modelo JSON
    for product_line in model_json['productLines']:
        for model in product_line['domainEngineering']['models']:
            for element in model['elements']:
                if element['id'] in feature_values:
                    for prop in element['properties']:
                        if prop['name'] == 'Selected':
                            prop['value'] = feature_values[element['id']]

    return model_json
# Use the function
#json_data = read_json_file('test.json')
#config_json = read_json_file('configurations.json')
#model_id = "a3d70a9f-05cc-4b72-a51c-c53abb7b467e"
#json_response = apply_configuration_to_model(json_data, config_json, "cb945915-35c3-46af-a72e-403f941f613c")
#write_json_to_file(json_response, 'model.json')
#config_output = extract_feature_info(json_data, model_id)
#write_json_to_file(config_output, 'configurations.json')
#print(json.dumps(config_output, indent=4))

#manage_configurations(json_data, model_id,"configuracion1",config_json)
#manage_configurations(json_data, model_id,"configuracion2",config_json)
#write_json_to_file(config_json, 'configurations.json')

#print(config_json)