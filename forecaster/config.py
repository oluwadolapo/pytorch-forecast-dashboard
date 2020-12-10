import argparse

def get_params():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--best_model_path', dest='best_model_path', type=str, default=None,
                        help='Model path for best model')
    
    args = parser.parse_args()
    return args