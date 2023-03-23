import numpy as np
import nibabel as nib
import pandas as pd
from copy import deepcopy


# SynthSeg ROI dictionary
def synthInfo():
    synth_rois = {'left thalamus':[], 'left caudate':[], 'left putamen':[], 'left pallidum':[], 'left hippocampus':[], 
    'right thalamus':[], 'right caudate':[],'right putamen':[], 'right pallidum':[], 'right hippocampus':[], 'csf':[]}
    values = np.load('synthseg_segmentation_labels_2.0.npy')
    names = np.load('synthseg_segmentation_names_2.0.npy')
    return synth_rois, values, names



# Analyzing difference
def dice(seg, gt):
    return (np.sum(seg[gt!=0])*2)/(np.sum(seg) + np.sum(gt))
def diceK(seg, gt, k):
    return (np.sum(seg[gt==k])*2)/(np.sum(seg) + np.sum(gt))


# Generating and saving statistics

# Input: dictionary = {k1: [v1,v2,v3], k2: [v1,v2,v3]}
# Saves an excel file with mean and std of each list
def dictToExcel(stats_dict, name):
    data = {}
    for key, value in stats_dict.items():
        data[key]  = [np.mean(value), np.std(value)]
    df = pd.DataFrame(data=data, index= ['mean', 'std'])
    df.to_excel(name+'_stats.xlsx')

    
    
# Extract qsm mean and median values
def extractQSM(subjects, path, path_seg, path_qsm, label):
    print('Running extractQSM for '+ str(len(subjects)) + ' subjects with label ' + label)
    print('QSM: ' + path_qsm + '\nSegment: ' + path_seg)
    synthRois, values, names = synthInfo()
    roi_mean = deepcopy(synthRois)
    roi_median = deepcopy(synthRois)
    
    for s in subjects:
        print('subject: ' + s)
        seg_path = path + s + path_seg
        qsm_path = path + s + path_qsm
        #stats_path_s = label + '_stats_subject_' + s + '.xlsx'
        qsm = nib.load(qsm_path).get_fdata()
        seg = nib.load(seg_path).get_fdata()
        #stats = {}
        for i in range(len(values)):
            if names[i] in synthRois:
                seg_i = np.extract(seg == values[i], qsm)
                seg_i_mean = np.mean(seg_i)
                seg_i_median = np.median(seg_i)
                roi_mean[names[i]].append(seg_i_mean)
                roi_median[names[i]].append(seg_i_median)
                #stats[i] = [names[i],values[i],seg_i_mean, seg_i_median, np.std(seg_i)]               
        #df = pd.DataFrame(data=stats, index= ['Structure name','Segment value','QSM mean', 'QSM median', 'STD']).T
        #df.to_excel(stats_path_s)
    dictToExcel(roi_mean, label + '_mean_total')
    dictToExcel(roi_median, label + '_median_total')
    
    df_roi = pd.DataFrame(data=roi_mean)
    df_roi.to_excel(label +'_all_subjects_stats_mean.xlsx')
    df_roi = pd.DataFrame(data=roi_median)
    df_roi.to_excel(label +'_all_subjects_stats_median.xlsx')
    print('Done')

































