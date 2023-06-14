#                          *****************************************************
# ~~~~~~~~~~~~~~~~~~~~~~~~ ALLY'S CODE FOR SORTING DETECTIONS AND NON DETECTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                          *****************************************************
# created June 13 2023

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def sort_detections(data_set, ion, vir_rad):
    #rho rvir cut
    cut1= data_set[data_set['rho_rvir']<= vir_rad]
    #threshold cut; take values with thresh less than 13.5 bc any higher value leaves too much room for noise
    cut2= cut1[cut1[ion+'_log10_N_det_thresh']<13.5]
    # cut to only include the detections (they have associated column densities)
    detections = cut2[cut2[ion+'_total_log10_N'] > 0]
    #rho_rvir_detections= detections['rho_rvir']
    max_rho_rvir= max(detections['rho_rvir'])
    print(f"The max rho_rvir value in this data set is {max_rho_rvir}")
    #az_angle_detections= detections['azimuthal_angle']
    xvals_detect = detections['rho_rvir'] * np.sin(detections['azimuthal_angle'] * (np.pi / 180))
    yvals_detect= detections['rho_rvir'] * np.cos(detections['azimuthal_angle'] * (np.pi / 180))
    detections['xval_detect']= xvals_detect
    detections['yval_detect']= yvals_detect
    # These are the values that we will be plotting, update this in the parameters
    detections_length= len(detections)
    print(f"The total number of detections is {detections_length}")
    return detections

def safe_non_detections(data_set, ion, vir_rad):
    #rho rvir cut
    cut1= data_set[data_set['rho_rvir']<= vir_rad]
    #threshold cut; take values with thresh less than 13.5 bc any higher value leaves too much room for noise
    cut2= cut1[cut1[ion+'_log10_N_det_thresh']<13.5]
    # cut to only include the detections (they have associated column densities)
    non_detections_1= cut2[cut2['N_'+ion+'_components'] == 0]
    #this is the safe way to include all non detections
    non_detections_2= cut1[cut1[ion+'_total_log10_N']<cut1[ion+'_log10_N_det_thresh']]
    # was originally going to include those with data that is too noisy but taking this out for now
    # non_detections_3= cut1[cut1[ion+'_log10_N_det_thresh']>13.5]
    safe_nondetections= pd.concat([non_detections_1, non_detections_2])
    length_safe= len(safe_nondetections)
    print(f"The total number of safe non detections is {length_safe}. (This includes galaxies with 0 components and those with values below their own detections threshold)")
    xvals_detect_snd= safe_nondetections['rho_rvir'] * np.sin(safe_nondetections['azimuthal_angle'] * (np.pi / 180))
    yvals_detect_snd= safe_nondetections['rho_rvir'] * np.cos(safe_nondetections['azimuthal_angle'] * (np.pi / 180))
    safe_nondetections['xval_detect']= xvals_detect_snd
    safe_nondetections['yval_detect']= yvals_detect_snd
    return safe_nondetections

def basic_non_detections(data_set, ion, vir_rad):
    #rho rvir cut
    cut1= data_set[data_set['rho_rvir']<= vir_rad]
    # cut to only include the detections (they have associated column densities)
    non_detections_1= cut1[cut1['N_'+ion+'_components'] == 0]
    # including those with data that is too noisy (taking this out for now)
    # non_detections_2= cut1[cut1[ion+'_log10_N_det_thresh']>13.5]
    #basic_nondetections= pd.concat([non_detections_1, non_detections_2])
    length_basic= len(non_detections_1)
    print(f"The total number of basic non detections is {length_basic}. (This means that it only includes galaxies with 0 components)")
    xvals_detect_basic= non_detections_1['rho_rvir'] * np.sin(non_detections_1['azimuthal_angle'] * (np.pi / 180))
    yvals_detect_basic= non_detections_1['rho_rvir'] * np.cos(non_detections_1['azimuthal_angle'] * (np.pi / 180))
    non_detections_1['xval_detect']= xvals_detect_basic
    non_detections_1['yval_detect']= yvals_detect_basic
    return non_detections_1


def make_plot(data_set, detections, non_detections, ion, color_bar, cmap_color, set_xmax, set_ymax, set_vmin=None, set_vmax=None, set_title=None):
    plt.plot(np.linspace(0, 10, 100), np.linspace(0, 10, 100), c='k', ls='--', alpha=0.5, zorder=2)
    # add label for 45 degrees
    plt.text(.58, .72, '45$\degree$', fontsize=14, transform=plt.gcf().transFigure)
    color_bar_points = detections[color_bar]
    detection_points = plt.scatter(detections['xval_detect'], detections['yval_detect'], c=color_bar_points, zorder=4, marker='s', edgecolor='k', s=40, vmin= set_vmin, vmax= set_vmax, cmap= cmap_color, label= (ion+' detections'))
    nondetection_point= plt.scatter(non_detections['xval_detect'], non_detections['yval_detect'], edgecolor='k', s=30, color= 'gray', zorder=3, marker= '^', label= 'Non Detections')
    plt.xlim(0, set_xmax)
    plt.ylim(0, set_ymax)
    plt.xlabel(r'$\frac{\rho}{r_{vir}}$', fontsize=20)
    plt.ylabel(r'$\frac{\rho}{r_{vir}}$', fontsize=20)
    plt.title(set_title, size=20)
    cbar = plt.colorbar(detection_points)
    cbar.set_label(color_bar, size=12)
    plt.text(0.13, .85, 'Along pole', fontsize=12, transform=plt.gcf().transFigure) 
    plt.text(0.58, .13, 'Along disk', fontsize=12, transform=plt.gcf().transFigure)
    plt.grid()
    plt.legend(loc='upper right');
