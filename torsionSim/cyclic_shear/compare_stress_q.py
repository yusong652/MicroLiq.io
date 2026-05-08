import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import style as st
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

# Critical-state slope sourced from Verdugo & Ishihara (1996) for
# Toyoura sand: their drained triaxial-compression dataset (b = 0)
# gives a steady-state friction angle phi_cs ~= 31 deg, which converts
# to the present HCA pure-shear loading (b = 0.5) via the
# Mohr-Coulomb relation M_cs = sqrt(3) * sin(phi_cs).
_PHI_CS_DEG_VI = 31.0

# setting style
# st.use("seaborn-deep")
csr_arr = [0.200]
k0s = [0.5, 0.67, 1.0, 1.5, 2.0]
markers = ['d', 's', 'o', '^', 'v']
colors = ['tab:orange', 'tab:red', 'tab:blue', 'tab:purple', 'tab:green']
linestyles = ['-.', ':', '-', '--', ':']

fig1 = plt.figure(figsize=(6,4))
ax1 = plt.gca()
FS_LABEL = 15
FS_TICK = 14
FS_LEGEND = 14
FS_ANN = 14
LW_MAIN = 1.5

def draw_dev(k0, lst, color):
	for csr in csr_arr:
		file_name = "Dr90/k%.2f/csr_%.3f/torsion_shear.csv"%(k0, csr)
		print(file_name)
		try:
			df1 = pd.read_csv(file_name,header=0)
			print("Found")
		except FileNotFoundError:
			print("Not found")
			continue

		strains = df1["strain_shear"] * 100.0
		# overall data
		stresses_shear = df1["stress_shear"] / 1000.
		stresses_out = df1["stress_outer"] / 1000.
		stresses_in =df1["stress_inner"] / 1000.
		stresses_lat = (stresses_out + stresses_in) / 2.0
		stress_ini = stresses_out[0] + stresses_in[0] / 2.0
		stresses_u = -(stresses_in + stresses_out) / 2 + stress_ini
		stresses_z = df1["stress_z"] / 1000.0
		J2s = (1.0/6.0 * ((stresses_z-stresses_lat)**2 + 
			(stresses_z-stresses_lat)**2) + stresses_shear**2)
		stresses_dev = np.sqrt(3.0 * J2s)
		stresses_p = (stresses_in + stresses_out + stresses_z) / 3.0
		# measurement ball data
		time = df1["time_duration"]
		###################################################
		#  find the index when liquefaction occurs
		period = 1.0 / 8.0
		ind_liq = 0
		while stresses_u[ind_liq] < 0.95 * stress_ini:
			ind_liq += 1
		time_liq = time[ind_liq]
		##################################
		flt = time < 1.05 * time_liq
		ax1.plot(stresses_p[flt][::16],stresses_dev[flt][::16],linewidth=LW_MAIN,
			label=r"$K_0=%.2f$"%k0, color=color, linestyle=lst)

M_CS = float(np.sqrt(3.0) * np.sin(np.radians(_PHI_CS_DEG_VI)))


def draw_csl():
	p_max = 120.0
	ax1.plot([0.0, p_max], [0.0, M_CS * p_max],
		linewidth=LW_MAIN,
		label=(r"$Critical\ state\ line$" + "\n"
			+ r"$M_{cs}=%.3f$" % M_CS),
		color='tab:red', linestyle='--')

# ax1.set_title(r"$Triaxial\ Compression$")
# xmajorLocator = MultipleLocator(5)
# xmajorFormatter = FormatStrFormatter('%5.0f')
# ymajorLocator = MultipleLocator(1000)
# ymajorFormatter = FormatStrFormatter('%1.1f')
# ax1.xaxis.set_major_locator(xmajorLocator)
# ax1.xaxis.set_major_formatter(xmajorFormatter)
# ax1.yaxis.set_major_locator(ymajorLocator)
# ax1.yaxis.set_major_formatter(ymajorFormatter)
# xminorLocator = MultipleLocator(1)
# yminorLocator = MultipleLocator(200)
# ax1.xaxis.set_minor_locator(xminorLocator)
# ax1.yaxis.set_minor_locator(yminorLocator)
for k0, lst, color in zip(k0s, linestyles, colors):
	draw_dev(k0, lst, color)

# Capture K0 cyclic handles before adding the CSL line, so the two
# legends can be placed independently.
k0_handles = list(ax1.lines)
draw_csl()
csl_handle = ax1.lines[-1]

ax1.set_xlim(0.0, 110.0)
ax1.set_ylim((-0, 100))
ax1.grid(axis='both',which='major',color='grey',linestyle='--',
	lw=0.35,alpha=0.8)
ax1.grid(axis='y',which='minor',color='grey',linestyle='--',
	lw=0.35,alpha=0.8)
ax1.set_ylabel(r'$Deviatoric\ stress\ q\ (kPa)$', fontsize=FS_LABEL)
ax1.set_xlabel(r'$Mean\ effective\ stress\ p\prime\ (kPa)$', fontsize=FS_LABEL)
# K0 cyclic legend (with CSR shown as the title) at upper-left;
# CSL legend at upper-right where the wedge between cyclic data and
# the CSL line is empty.
legend_k0 = ax1.legend(handles=k0_handles, fontsize=FS_LEGEND,
	framealpha=0.5, loc='upper left',
	title=r"$CSR=0.200$", title_fontsize=FS_LEGEND)
ax1.add_artist(legend_k0)
ax1.legend(handles=[csl_handle], fontsize=FS_LEGEND,
	framealpha=0.5, loc='upper right')
ax1.tick_params(axis='both', which='major', labelsize=FS_TICK)

plt.tight_layout()
plt.savefig("stress_dev.png",dpi=350)
plt.show()
