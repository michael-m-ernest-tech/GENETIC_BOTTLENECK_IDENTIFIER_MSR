"""Generate a small, reproducible dummy genetic dataset for a conservation study."""

from pathlib import Path
import random

import pandas as pd


SEED = 20261008
ALLELES = (142, 146, 150)
LOCUS_COUNT = 5
BOTTLENECK_COUNT = 15


def generate_population() -> pd.DataFrame:
    rng = random.Random(SEED)
    rows = []

    for individual_number in range(1, 31):
        row = {"Individual_ID": f"Bear_{individual_number:02d}"}

        if individual_number <= BOTTLENECK_COUNT:
            # The bottleneck cohort is homozygous at every locus. Allele 142
            # is more common, representing reduced variation in this cohort.
            genotypes = []
            for _ in range(LOCUS_COUNT):
                allele = rng.choices(ALLELES, weights=(0.7, 0.2, 0.1), k=1)[0]
                genotypes.append((allele, allele))
        else:
            # Give each comparison individual at least three heterozygous
            # loci so the two halves have visibly different diversity.
            while True:
                genotypes = [
                    (
                        rng.choices(ALLELES, weights=(0.5, 0.3, 0.2), k=1)[0],
                        rng.choices(ALLELES, weights=(0.5, 0.3, 0.2), k=1)[0],
                    )
                    for _ in range(LOCUS_COUNT)
                ]
                if sum(allele_1 != allele_2 for allele_1, allele_2 in genotypes) >= 3:
                    break

        for locus_number, (allele_1, allele_2) in enumerate(genotypes, start=1):
            row[f"Locus{locus_number}_A1"] = allele_1
            row[f"Locus{locus_number}_A2"] = allele_2

        rows.append(row)

    columns = ["Individual_ID"] + [
        f"Locus{locus_number}_{allele_copy}"
        for locus_number in range(1, LOCUS_COUNT + 1)
        for allele_copy in ("A1", "A2")
    ]
    return pd.DataFrame(rows, columns=columns)


def main() -> None:
    output_path = Path(__file__).resolve().parent / "test_population.csv"
    population = generate_population()
    population.to_csv(output_path, index=False)
    print(f"Wrote {len(population)} individuals to {output_path}")


if __name__ == "__main__":
    main()
