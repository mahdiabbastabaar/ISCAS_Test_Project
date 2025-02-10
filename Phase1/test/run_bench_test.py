import pytest
import os
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
    # Predicate 5:
    ('OR', '0', '0', '0'),  # Test1 (+ Predicate 6: Test4)
    ('OR', '0', '1', '1'),  # Test2
    ('OR', '1', '0', '1'),  # Test3
    ('OR', '1', '1', '1'),  # Test4
    # Predicate 6:
    ('OR', 'U', 'U', 'U'),  # Test1
    ('OR', 'U', '0', 'U'),  # Test2
    ('OR', '0', 'U', 'U'),  # Test3
    # Predicate 7:
    ('XOR', '1', '0', '1'),  # Test1
    ('XOR', '1', 'U', 'U'),  # Test2
    ('XOR', 'U', '1', 'U'),  # Test3
    ('XOR', 'U', 'U', 'U'),  # Test4
    # Predicate 8:
    ('XOR', '0', '0', '0'),  # Test1
    ('XOR', '1', '1', '0'),  # Test2
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


@pytest.mark.parametrize("test_id", range(1, 14))
def test_isp(test_id):
    """Test the conversion of ISC files to BENCH format"""

    isc_file_in = f"Phase1/test/isp_files/isc/test{test_id}.isc"
    bench_file_exp = f"Phase1/test/isp_files/bench_expected/test_exp{test_id}.bench"
    bench_file_out = f"Phase1/test/isp_files/bench_real/test{test_id}.bench"

    # for local testing

    # isc_file_in = f"isp_files/isc/test{test_id}.isc"
    # bench_file_exp = f"isp_files/bench_expected/test_exp{test_id}.bench"
    # bench_file_out = f"isp_files/bench_real/test{test_id}.bench"

    print(f"\nRunning Test {test_id}: {isc_file_in}")

    assert os.path.exists(isc_file_in), f"Input file missing: {isc_file_in}"
    assert os.path.exists(bench_file_exp), f"Expected output file missing: {bench_file_exp}"

    phaseOne.isc_to_bench(isc_file_in, bench_file_out)

    with open(bench_file_exp, "r") as file:
        expected_val = file.read().splitlines()[1:]
    with open(bench_file_out, "r") as file:
        real_val = file.read().splitlines()[1:]

    assert real_val == expected_val, f"Test {test_id} failed: Output does not match expected"
