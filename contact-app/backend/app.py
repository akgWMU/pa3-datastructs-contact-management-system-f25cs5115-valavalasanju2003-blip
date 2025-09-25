from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import io
import matplotlib.pyplot as plt
from flask_cors import CORS

from data_structures.contact import Contact
from data_structures.array_store import ArrayStore
from data_structures.linkedlist_store import LinkedListStore
from data_structures.bst_store import BSTStore
from data_structures.hashmap_store import HashMapStore
from data_structures.heap_store import HeapStore
from benchmark import run_benchmarks
from data_structures.complexities import complexities


app = Flask(__name__, static_folder="../frontend")
CORS(app)  # allow frontend JS to call backend

# ---------------- Static File Routes ---------------- #

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

# ---------------- Data Structure Initialization ---------------- #

stores = {
    "array": ArrayStore(),
    "linkedlist": LinkedListStore(),
    "bst": BSTStore(),
    "hashmap": HashMapStore(),
    "heap": HeapStore(),
}

def get_store(ds):
    return stores.get(ds)

# ---------------- API Routes ---------------- #

@app.route("/insert", methods=["POST"])
def insert():
    data = request.json
    ds = get_store(data["ds"])
    if not ds:
        return jsonify({"error": "Invalid data structure"}), 400
    contact = Contact(data["name"], data["phone"], data["email"])
    ds.insert(contact)
    return jsonify({"status": "success", "contact": contact.__dict__})

@app.route("/search/<ds>/<name>", methods=["GET"])
def search(ds, name):
    store = get_store(ds)
    if not store:
        return jsonify({"error": "Invalid data structure"}), 400
    contact = store.search(name)
    if contact:
        return jsonify(contact.__dict__)
    return jsonify({"error": "Contact not found"}), 404

@app.route("/delete/<ds>/<name>", methods=["DELETE"])
def delete(ds, name):
    store = get_store(ds)
    if not store:
        return jsonify({"error": "Invalid data structure"}), 400
    deleted = store.delete(name)
    if deleted:
        return jsonify({"status": "deleted", "name": name})
    return jsonify({"error": "Contact not found"}), 404

@app.route("/update", methods=["PUT"])
def update():
    data = request.json
    store = get_store(data["ds"])
    if not store:
        return jsonify({"error": "Invalid data structure"}), 400
    
    contact = store.search(data["old_name"])
    if not contact:
        return jsonify({"error": "Contact not found"}), 404

    # Update fields
    contact.name = data.get("new_name", contact.name)
    contact.phone = data.get("new_phone", contact.phone)
    contact.email = data.get("new_email", contact.email)

    return jsonify({"status": "updated", "contact": contact.__dict__})

@app.route("/list/<ds>", methods=["GET"])
def list_contacts(ds):
    store = get_store(ds)
    if not store:
        return jsonify({"error": "Invalid data structure"}), 400
    contacts = [c.__dict__ for c in store.list_all()]
    return jsonify(contacts)

# ---------------- Benchmark Route ---------------- #
@app.route("/full_benchmark", methods=["GET"])
def full_benchmark():
    df = run_benchmarks()
    complexities_table = complexities
    return jsonify({
        "complexities": complexities_table,
        "results": df.to_dict(orient="records")
    })

@app.route("/benchmark", methods=["GET"])
def benchmark():
    n = int(request.args.get("n", 2000))
    df = run_benchmarks(n)

    img = io.BytesIO()
    df.plot(kind="bar", figsize=(10, 6))
    plt.title(f"Performance Comparison ({n} operations)")
    plt.ylabel("Time (seconds)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(img, format="png")
    img.seek(0)

    return send_file(img, mimetype="image/png")

# ---------------- Run ---------------- #

if __name__ == "__main__":
    app.run(debug=True)
