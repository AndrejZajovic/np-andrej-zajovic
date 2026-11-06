def prosjecna_ocjena(ocjene: list[int | float]) -> float:
    """Vraća aritmetičku sredinu liste ocjena.

    Args:
        ocjene: lista ocjena (cijeli ili decimalni brojevi).

    Returns:
        Prosječna ocjena kao float.

    Raises:
        ValueError: ako je lista prazna.
    """
    if not ocjene:
        raise ValueError("Lista ocjena ne smije biti prazna.")
    return sum(ocjene) / len(ocjene)
