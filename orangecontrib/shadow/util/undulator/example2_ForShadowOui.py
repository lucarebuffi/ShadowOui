#
# examples for SourceUndulator to be used in ShadowOui
#

import os
from syned.storage_ring.electron_beam import ElectronBeam
from syned.storage_ring.magnetic_structures.undulator import Undulator
from orangecontrib.shadow.util.undulator.SourceUndulator import SourceUndulator
if __name__ == "__main__":

    do_plots = True
    #
    # syned
    #
    su = Undulator.initialize_as_vertical_undulator(K=0.25,period_length=0.032,periods_number=50)

    ebeam = ElectronBeam(energy_in_GeV=6.04,
                 energy_spread = 0.0,
                 current = 0.2,
                 number_of_bunches = 400,
                 moment_xx=(400e-6)**2,
                 moment_xxp=0.0,
                 moment_xpxp=(10e-6)**2,
                 moment_yy=(10e-6)**2,
                 moment_yyp=0.0,
                 moment_ypyp=(4e-6)**2 )

    sourceundulator = SourceUndulator(name="test",syned_electron_beam=ebeam,syned_undulator=su,
                    FLAG_EMITTANCE=1,FLAG_SIZE=0,
                    EMIN=10490.0,EMAX=10510.0,NG_E=3,
                    MAXANGLE=0.015,NG_T=51,NG_P=11,NG_J=20,
                    SEED=36255,NRAYS=15000,
                    code_undul_phot="internal")


    sourceundulator.set_energy_monochromatic_at_resonance(0.98)

    print(sourceundulator.info())

    #
    # plot
    #
    if do_plots:
        from srxraylib.plot.gol import plot_image, plot_scatter

        radiation,theta,phi = sourceundulator.get_radiation_polar()
        plot_image(radiation[0],1e6*theta,phi,aspect='auto',title="intensity",xtitle="theta [urad]",ytitle="phi [rad]")

        radiation_interpolated,vx,vz = sourceundulator.get_radiation_interpolated_cartesian()
        plot_image(radiation_interpolated[0],vx,vz,aspect='auto',title="intensity interpolated in cartesian grid",xtitle="vx",ytitle="vy")

        polarization = sourceundulator.result_radiation["polarization"]
        plot_image(polarization[0],1e6*theta,phi,aspect='auto',title="polarization",xtitle="theta [urad]",ytitle="phi [rad]")


    beam = sourceundulator.calculate_shadow3_beam(user_unit_to_m=1.0)

    print(sourceundulator.info())

    os.system("rm -f begin.dat start.00 end.00")
    beam.write("begin.dat")
    print("File written to disk: begin.dat")

    for k in sourceundulator.result_radiation.keys():
        print(k)

    print("Beam intensity: ",beam.getshcol(23).sum())
    print("Beam intensity s-pol: ",beam.getshcol(24).sum())
    print("Beam intensity: p-pol",beam.getshcol(25).sum())

    #
    # plot
    #
    if do_plots:
        plot_scatter(1e6*beam.rays[:,0],1e6*beam.rays[:,2],title="real space",xtitle="X [um]",ytitle="Z [um]",show=False)
        plot_scatter(1e6*beam.rays[:,3],1e6*beam.rays[:,5],title="divergence space",xtitle="X [urad]",ytitle="Z [urad]",show=True)

