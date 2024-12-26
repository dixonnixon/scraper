import importlib
import yaml

import importlib.util
import threading

def import_module(module_name):
    spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module



def singleton(cls):
    instances = {}
 
    def wrapper(*args, **kwargs):
        #print(cls, instances)
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper

def create_instance(class_name, *args, **kwargs):
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
        allowed_classes = config['allowed_classes']

    if class_name not in allowed_classes:
        raise ValueError(f"Invalid class name: {class_name}")

    module_name, class_name = class_name.rsplit(".", 1)
    module = importlib.import_module(module_name)
    #module = import_module(module_name)  # Use dynamic import for flexibility
    klass = getattr(module, class_name)

    klass = singleton(klass)
    # Apply the singleton decorator to the class
    instance = klass(*args, **kwargs)

    #return instance(*args, **kwargs)
    return instance
