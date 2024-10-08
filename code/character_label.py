#  Code to compute labels of mod-ell Dirichlet characters, and
#  construct such characters from their labels.
#
#  Original version by Peter Bruin 2017-04-06
#  Revised by John Cremona 2014-08-19 using enhanced Sage functionality
#
#######################################################################
#
# Copyright 2024 Peter Bruin, John Cremona
#
# This is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
#
#######################################################################


def dirichlet_character_label(chi):
    """
    Return the LMFDB label of ``chi``.

    The label is 'l.N.c' for a character modulo `N` with values in a
    finite field of characteristic `l`, with Conrey label `c`.

    INPUT:

    - ``chi`` -- a :class:`DirichletCharacter` with values in a finite
      field

    TESTS::

        sage: G = DirichletGroup(55, GF(11))
        sage: chi = G([1, 2])
        sage: dirichlet_character_label(chi)
        '11.55.46'

    """
    G = chi.parent()
    N = G.modulus()
    l = G.base_ring().characteristic()
    c = chi.conrey_number()
    return f"{l}.{N}.{c}"

def dirichlet_character_from_label(label):
    """
    Return the Dirichlet character with the given LMFDB label.

    The label 'l.N.c' denotes the character modulo `N` with values in
    a finite field of characteristic `l`, with Conrey label `c`.  To
    be valid, `c` must be coprime to `l`.

    TESTS::

        sage: chi = dirichlet_character_from_label('11.55.46')
        sage: chi(12)
        1
        sage: chi(46)
        2

    """
    l, N, c = (ZZ(v) for v in label.split("."))
    if c<0 or c>=N or c.gcd(N)>1:
        raise ValueError(f"{label} is not a valid label: {c} should be in the range 0..{N-1} and coprime to {N}")
    m = Mod(c, N).multiplicative_order()     # order of chi
    if m%l==0:
        raise ValueError(f"{label} is not a valid label: the order {m} of {c} modulo {N} should not be divisible by {l}")
    d = Mod(l, m).multiplicative_order()     # extension degree
    F = GF(l**d, modulus='conway', name='a') # value field
    a = F.gen()
    G = DirichletGroup(ZZ(N), F, zeta=a)
    z = a**(G.zeta_order() / m)
    H = pari.znstar(N,1)
    chi = G([z**(m*H.chareval(c, g)) for g in G.unit_gens()])
    return chi

def all_dirichlet_characters(l, N):
    """
    Return labels and values for all Dirichlet characters modulo `N`
    with values in a suitable finite field of characteristic `l`.

    TESTS::

        sage: all_dirichlet_characters(7, 5)
        [['7.5.1', [0, 1, 1, 1, 1]],
         ['7.5.2', [0, 1, 6*a + 4, a + 3, 6]],
         ['7.5.4', [0, 1, 6, 6, 1]],
         ['7.5.3', [0, 1, a + 3, 6*a + 4, 6]]]
        sage: def test(l, N):
        ....:     labels = [x[0] for x in all_dirichlet_characters(l, N)]
        ....:     chars = [dirichlet_character_from_label(lab) for lab in labels]
        ....:     return labels == [dirichlet_character_label(chi) for chi in chars]
        sage: test(3, 8)
        True
        sage: test(11, 55)
        True
        sage: test(11, 121)
        True
    """
    U = Zmod(N).unit_group()
    d = Mod(l, U.exponent().prime_to_m_part(l)).multiplicative_order()
    F = GF(l**d, modulus='conway', name='a')
    a = F.gen()
    G = DirichletGroup(N, F, zeta=a)
    return [[dirichlet_character_label(chi), chi.values()] for chi in G]

def galois_character_label(chi):
    """
    Return the LMFDB label of `\\chi`.

    INPUT:

    - ``chi`` -- a Galois character with values in a finite field
    """
    raise NotImplementedError
