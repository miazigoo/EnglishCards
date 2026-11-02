"""tests/examples/test_benchmark_examples.py

Executes the code snippets of the 5 benchmark cards in Python 3.12+ to verify
they run without syntax or runtime errors.
"""

def test_benchmark_rsplit_execution():
    filename = 'report.final.csv'
    assert filename.rsplit('.', 1) == ['report.final', 'csv']
    assert filename.split('.', 1) == ['report', 'final.csv']

def test_benchmark_zip_execution():
    names = ['Anna', 'Max']
    scores = [90, 85, 70]
    result = list(zip(names, scores))
    assert result == [('Anna', 90), ('Max', 85)]

def test_benchmark_issubclass_execution():
    class Animal:
        pass

    class Dog(Animal):
        pass

    assert issubclass(Dog, Animal) is True
    assert issubclass(Animal, Dog) is False
    assert issubclass(Dog, Dog) is True

def test_benchmark_getattr_execution():
    class Order:
        total_weight = 12.5

    order = Order()
    assert getattr(order, 'total_weight', 0.0) == 12.5
    assert getattr(order, 'missing_weight', 0.0) == 0.0

def test_benchmark_filter_execution():
    numbers = [-2, 0, 3, 5]
    result = list(filter(lambda n: n >= 0, numbers))
    assert result == [0, 3, 5]
