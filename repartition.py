import sys
import os


def merge(origin, target):
    rows = 0
    nnz = 0

    with (open(origin + "/processor0/0.0005/p_local_A_0.mtx", "r") as f0,
          open(origin + "/processor0/0.0005/p_local_A_1.mtx", "r") as f1,
          open(origin + "/processor0/0.0005/p_local_A_2.mtx", "r") as f2):

        token = f0.readlines()[1].split()
        rows = int(token[0])
        nnz += int(token[2])

        token = f1.readlines()[1].split()
        nnz += int(token[2])
        token = f2.readlines()[1].split()
        nnz += int(token[2])

    _, times, _ = next(os.walk(target + "/processor0"))

    for time in times:
        if time == "constant":
            continue

        if time == "0":
            continue

        print(f"processing {time}")

        with (open(origin + "/processor0/0.0005/p_local_A_1.mtx", "r") as ol1,
            open(origin + "/processor0/0.0005/p_local_A_2.mtx", "r") as ol1,
            open(target + f"/processor0/{time}/p_local_A_0.mtx", "r") as p1,
            open(target + f"/processor1/{time}/p_local_A_0.mtx", "r") as p2,
            open(target + f"/processor0/{time}/p_non_local_A_0.mtx", "r") as nl1,
            open(target + f"/processor1/{time}/p_non_local_A_0.mtx", "r") as nl2,
            open(target + f"/processor0/{time}/combined.mtx", "w") as out): 

            # write header
            out.write("%%MatrixMarket matrix coordinate real general\n")
            out.write(f"{rows} {rows} {nnz}\n")

            # just take p1 as is
            p1_lines = p1.readlines()
            for i, line in enumerate(p1_lines[2:]):
                out.write(line)

            p2_lines = p2.readlines()
            for line in p2_lines[2:]:
                row, col, coeff = line.split()
                out.write(f"{int(row) + i} {int(col) +i} {coeff}\n")

            # add non_local_0 with rows, cols from local_1
            ol1_lines = ol1.readlines()
            nl1_lines = ol1.readlines()
            for ol1_line, nl1_line in zip(ol1_lines[2:],nl1_lines[2:]):
                token_ol1 = ol1_line.split()
                token_nl1 = nl1_line.split()
                out.write(f"{token_ol1[0]} {token_ol1[1]} {token_nl1[2]}\n")

            # add non_local_0 with rows, cols from local_1
            ol1_lines = ol1.readlines()
            nl1_lines = ol1.readlines()
            for ol1_line, nl1_line in zip(ol1_lines[2:],nl1_lines[2:]):
                token_ol1 = ol1_line.split()
                token_nl1 = nl1_line.split()
                out.write(f"{token_ol1[0]} {token_ol1[1]} {token_nl1[2]}\n")


def main():
    origin = sys.argv[1]
    target = sys.argv[2]
    merge(origin, target)


if __name__ == "__main__":
    main()
