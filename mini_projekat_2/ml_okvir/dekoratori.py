"""Decorator: mjerenje vremena izvršavanja funkcije ili metode."""
import functools
import time


def mjeri_vrijeme(fn):
    """Mjeri trajanje poziva i čuva ga, a povratnu vrijednost ne mijenja.

    - trajanje se uvijek upisuje u ``omotac.zadnje_trajanje``
    - ako prvi argument (``self``) ima rječnik ``vremena``, trajanje se upisuje
      i u ``self.vremena[naziv_funkcije]``, pa je mjerenje po objektu.
    """

    @functools.wraps(fn)
    def omotac(*args, **kwargs):
        pocetak = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            trajanje = time.perf_counter() - pocetak
            omotac.zadnje_trajanje = trajanje
            if args and isinstance(getattr(args[0], "vremena", None), dict):
                args[0].vremena[fn.__name__] = trajanje

    omotac.zadnje_trajanje = None
    return omotac
