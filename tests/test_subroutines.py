from datablox.subroutines import mkdir_recursively
from random import randint

def test_mkdir_recursively():
    success_dir = "/tmp/test/%d-%d-%d/%d" % (
        randint(10000, 100000),
        randint(10000, 100000),
        randint(10000, 100000),
        randint(10000, 100000),
    )
    # This should succeed
    assert True == mkdir_recursively(
        success_dir
    )

    assert None == mkdir_recursively(
        success_dir
    )

    assert False == mkdir_recursively("/dblx")

if __name__ == "__main__":
    test_mkdir_recursively()