"""Per-contact dump for fabric-anisotropy analysis (full, no compression).

Dumps every contact (BallBall + BallFacet) at the listed time-step indices.
Filtering bb vs bf is done downstream so the same CSV supports both the
standard fabric analysis and a robust BallFacet vs BallBall boundary check.
"""
import os
import csv
import itasca as it
import numpy as np

OUT_DIR = 'contact_full'
INDICES = [0, 226, 379, 386]
DT = 0.01  # shear_time step matches np.linspace(0, 5.40, 541)


def export_contacts(idx):
    """Per-contact dump.

    Columns:
      contact_type         -- 'bb' (ball-ball) or 'bf' (ball-facet)
      pos_x, pos_y, pos_z  -- contact position (m)
      n_x,   n_y,   n_z    -- unit contact normal (from contact.normal())
      fn                   -- scalar normal force, |F_total . n_hat|  (N)
      ft                   -- scalar tangential force, |F_total - fn n_hat|  (N)

    Usage downstream:
      - Fabric tensor / anisotropy:   filter contact_type == 'bb' (standard)
      - Boundary-effect diagnostics:  contact_type == 'bf'
    """
    fname = os.path.join(OUT_DIR, 'contact_{}.csv'.format(idx))
    n_bb, n_bf, n_skip = 0, 0, 0
    with open(fname, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['contact_type',
                    'pos_x', 'pos_y', 'pos_z',
                    'n_x', 'n_y', 'n_z',
                    'fn', 'ft'])
        for c in it.contact.list():
            if c.__class__ == it.BallBallContact:
                ctype = 'bb'
                n_bb += 1
            elif c.__class__ == it.BallFacetContact:
                ctype = 'bf'
                n_bf += 1
            else:
                n_skip += 1
                continue
            pos = c.pos()
            n = np.array(c.normal())
            F = np.array(c.force_global())
            fn_signed = float(np.dot(F, n))
            Ft = F - fn_signed * n
            w.writerow([ctype,
                        pos[0], pos[1], pos[2],
                        n[0], n[1], n[2],
                        abs(fn_signed),
                        float(np.linalg.norm(Ft))])
    print('  wrote {}: bb={} bf={} skipped={}'.format(fname, n_bb, n_bf, n_skip))


def main():
    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    for idx in INDICES:
        time = round(idx * DT, 2)
        state_name = 'shear_time_{}'.format(time)
        print('--- restoring {} (idx={}) ---'.format(state_name, idx))
        it.command("model restore '{}'".format(state_name))
        export_contacts(idx)
    print('done. files in {}'.format(OUT_DIR))


main()
