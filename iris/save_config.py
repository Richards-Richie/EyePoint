import pickle

# Define the configurations to be saved
config = {
    'LEFT_EYE': [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398],
    'RIGHT_EYE': [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246],
    'LEFT_IRIS': [474, 475, 476, 477],
    'RIGHT_IRIS': [469, 470, 471, 472]
}

# Save the configuration to a pickle file
with open('iris_detection_config.pkl', 'wb') as f:
    pickle.dump(config, f)

print("Configuration saved successfully.")
