complexities = {
    "array": {
        "insert": "O(1) amortized",
        "search": "O(n)",
        "delete": "O(n)",
        "list": "O(n)"
    },
    "linkedlist": {
        "insert": "O(1)",
        "search": "O(n)",
        "delete": "O(n)",
        "list": "O(n)"
    },
    "bst": {
        "insert": "O(log n) avg, O(n) worst",
        "search": "O(log n) avg, O(n) worst",
        "delete": "O(log n) avg, O(n) worst",
        "list": "O(n)"
    },
    "hashmap": {
        "insert": "O(1) avg, O(n) worst",
        "search": "O(1) avg, O(n) worst",
        "delete": "O(1) avg, O(n) worst",
        "list": "O(n)"
    },
    "heap": {
        "insert": "O(log n)",
        "search": "O(n)",
        "delete": "O(log n) for root, O(n) general",
        "list": "O(n log n) if sorted"
    }
}
