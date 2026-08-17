import pickle
from pathlib import Path

path = Path("models/baseline_xgboost.pkl")

print("=" * 70)
print("INSPECTING SAVED XGBOOST MODEL")
print("=" * 70)
print("File:", path.resolve())
print("Size:", path.stat().st_size, "bytes")

with open(path, "rb") as f:
    model = pickle.load(f)

print("\nMODEL TYPE")
print(type(model))

print("\nMODEL PARAMETERS")
try:
    print(model.get_params())
except Exception as e:
    print("Could not get params:", e)

print("\nMODEL ATTRIBUTES")

for attr in [
    "n_features_in_",
    "feature_names_in_",
    "n_estimators",
    "max_depth",
    "learning_rate",
    "subsample",
    "colsample_bytree",
]:
    try:
        value = getattr(model, attr)
        if attr == "feature_names_in_":
            print(attr, "=", list(value))
        else:
            print(attr, "=", value)
    except Exception:
        print(attr, "= <not available>")

print("\nOBJECT DICT KEYS")
try:
    print(list(model.__dict__.keys()))
except Exception as e:
    print(e)