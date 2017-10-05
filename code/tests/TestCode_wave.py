"""
    Forced-disspative QG: still testing.
"""
import timeit

import matplotlib.pyplot as plt
plt.rcParams['contour.negative_linestyle'] = 'dashed'
import numpy as np

from niwqg import CoupledModel
from niwqg import UnCoupledModel
from niwqg import InitialConditions as ic
import cmocean

from pyspec import spectrum

plt.close('all')

# parameters
nx = 128
f0 = 1.e-4
N = 0.005
L = 2*np.pi*200e3

λz = 400

m = 2*np.pi/λz
#nu4, nu4w = 3.5e7, 4.25e6 # hyperviscosity

# dissipation
Tmu = 200*86400
mu = 1./Tmu

dt = 0.00025*Tmu
tmax = 3*Tmu

#forcing
dk = 2*np.pi/L

kf = 8*dk
dkf = 1*dk

# energy input
U0 = 0.5
epsilon = (U0**2)*mu
sigma = np.sqrt(epsilon)

path = "output/test_wave"

# Force only dynamics
wavemodel = CoupledModel.Model(L=L,nx=nx, tmax = tmax,dt = dt, twrite=20,
                    nu4=0,mu=mu,nu4w=0,nu=0,nuw=0,muw=mu,tstorm=int(7*86400//dt), use_filter=True,save_to_disk=True,
                    tsave_snapshots=25,path=path,
                    U = 0., tdiags=1,
                    f=f0,N=N,m=m,
                    wavenumber_forcing=kf,width_forcing=dkf,
                    sigma_q = 0., sigma_w=.1 )

wavemodel.set_q(np.zeros([wavemodel.nx]*2))
wavemodel.set_phi(np.zeros([wavemodel.nx]*2)+0j)
wavemodel._invert()

# run the model
wavemodel.run()

# # plot spectrum and a realization of the forcing
# fig = plt.figure(figsize=(8.5,4.5))
# Q = (2*np.pi)**-2 * epsilon/(mu**2 / kf**2)
#
# ax = fig.add_subplot(121,aspect=1)
# plt.contourf(np.fft.fftshift(qgmodel.k)/kf,np.fft.fftshift(qgmodel.l)/kf,\
#                 1e3*np.fft.fftshift(qgmodel.spectrum_qg_forcing),40)
# plt.xlim(-2.5,2.5)
# plt.ylim(-2.5,2.5)
# plt.xlabel(r"$k/k_f$")
# plt.ylabel(r"$l/k_f$")
# plt.colorbar(orientation="horizontal",ticks=[0,2,4,6,8],shrink=0.8,\
#                 label=r"Power spectrum $[10^{-3}\,\, \mathcal{F}_{kl}]$")
#
# ax = fig.add_subplot(122,aspect=1)
# Lf = 2*np.pi/kf
# cf = np.linspace(-1,1,40)
# plt.contourf(qgmodel.x/Lf,qgmodel.y/Lf,1e6*np.fft.ifft2(qgmodel.forceh)/np.sqrt(qgmodel.dt)/Q,\
#                     cf,cmap=cmocean.cm.curl,extend='both')
# plt.colorbar(orientation="horizontal",shrink=0.8,ticks=[-1,-.5,0,.5,1.],\
#                 label=r"Realization of white-noise forcing [$10^{-6}\,\,\xi_q/Q$]")
# plt.xlabel(r'$x\, k_f/2\pi$')
# plt.ylabel(r'$y\, k_f/2\pi$')
#
# plt.savefig('figs/forcing_qg-only')
#
# # plot potential vorticity
# fig = plt.figure(figsize=(5.5,4))
# cv = np.linspace(-.2,.2,40)
#
# ax = fig.add_subplot(111,aspect=1)
# plt.contourf(qgmodel.x/Lf,qgmodel.y/Lf,qgmodel.q/Q,cv,\
#                 cmin=-0.2,cmax=0.2,extend='both',cmap=cmocean.cm.curl)
# plt.colorbar(ticks=[-.2,-.1,0,.1,.2],label=r'Potential vorticity $[q/Q]$')
# plt.xlabel(r'$x\, k_f/2\pi$')
# plt.ylabel(r'$y\, k_f/2\pi$')
# plt.savefig('figs/snapshots_pv_qg-only')
#
# diagnostics
time = wavemodel.diagnostics['time']['value']
dt = time[1]-time[0]
KE_qg = wavemodel.diagnostics['ke_qg']['value']
KE_niw = wavemodel.diagnostics['ke_niw']['value']
PE_niw = wavemodel.diagnostics['pe_niw']['value']

#energy_input = wavemodel.diagnostics['wave_energy_input']['value']
work = wavemodel.diagnostics['Work_w']['value']
#work2 = np.cumsum(energy_input*dt)

#
# ENS_qg = qgmodel.diagnostics['ens']['value']
# ep_psi = qgmodel.diagnostics['ep_psi']['value']
# smalldiss_psi = qgmodel.diagnostics['smalldiss_psi']['value']
#

# chi_q =  qgmodel.diagnostics['chi_q']['value']
#
# wave_energy_input = qgmodel.diagnostics['wave_energy_input']['value']
# ep_phi = qgmodel.diagnostics['ep_phi']['value']

# work
epsilon_w = (wavemodel.sigma_w**2)/2

fig = plt.figure(figsize=(8.5,4.))
ax = fig.add_subplot(111)
plt.plot(time*wavemodel.muw,work/time)
plt.plot(time*wavemodel.muw,work2/time)
plt.plot(time*wavemodel.muw,epsilon_w*np.ones_like(time))

# plot energy
fig = plt.figure(figsize=(8.5,4.))
E = epsilon_w/wavemodel.muw/4
ax = fig.add_subplot(111)
plt.plot(time*wavemodel.muw,KE_niw/E)
plt.plot(time*wavemodel.muw,np.ones_like(time),'r--')
plt.xlabel(r"Time $[t\,\,\mu]$")
plt.ylabel(r"Balanced kinetic energy $[\mathcal{K} \,\, 2 \gamma/\sigma_w^2]$")
plt.savefig('figs/kinetic_energy_wave-only')

# # calculate spectrum
# # calculate spectrum
# E = 0.5 * np.abs(qgmodel.wv*qgmodel.ph)**2
# ki, Er = spectrum.calc_ispec(qgmodel.kk, qgmodel.ll, E, ndim=2)
#

# dt = time[1]-time[0]
# dKE = np.gradient(KE_qg,dt)
# dKEw = np.gradient(KE_niw,dt)
