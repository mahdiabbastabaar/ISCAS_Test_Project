import pytest

from Phase1 import phaseOne

bench_format = """
INPUT(1)
INPUT(2)

OUTPUT(3)

3 = {gate}(1, 2)
"""

input_file_format = """ 1 2
{first} {second}
"""


def get_value_from_log(output_file, target_wire):
    with open(output_file, "r") as file:
        for line in file:
            key, value = line.strip().split(": ")
            if key == str(target_wire):
                return value
    return None


@pytest.mark.parametrize("gate, first, second, expected", [
    # Predicate 1:
    ('AND', '1', '1', '1'),  # Test1 (+ Predicate 2: Test4)
    ('AND', '1', '0', '0'),  # Test2
    ('AND', '0', '1', '0'),  # Test3
    ('AND', '0', '0', '0'),  # Test4
    # Predicate 2:
    ('AND', 'U', 'U', 'U'),  # Test1
    ('AND', 'U', '1', 'U'),  # Test2
    ('AND', '1', 'U', 'U'),  # Test3
    # Predicate 3:
    ('NOT', '0', '-', '1'),  # Test1 (+ Predicate 4: Test2)
    ('NOT', '1', '-', '0'),  # Test2
    # Predicate 4:
    ('NOT', 'U', '-', 'U'),  # Test1
    # BUFF:
    ('BUFF', '0', '-', '0'),  # Test1
    ('BUFF', '1', '-', '1'),  # Test2
    ('BUFF', 'U', '-', 'U'),  # Test3
])
def test_gate(gate, first, second, expected):
    bench_file = 'test.bench'
    input_file = 'test.pi'
    output_file = 'test.log'

    bench_content = bench_format.format(gate=gate)
    with open(bench_file, "w") as file:
        file.write(bench_content)

    input_file_content = input_file_format.format(first=first, second=second)
    with open(input_file, "w") as file:
        file.write(input_file_content)

    phaseOne.run_bench(bench_file, input_file, output_file)

    assert get_value_from_log(output_file, 3) == expected
