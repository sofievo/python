import numpy as np
import nibabel as nib
import pandas as pd
from copy import deepcopy
import csv



# Helper functions
def loadNifti(path):
    data = nib.load(path).get_fdata()
    return data


# SynthSeg ROI dictionary, labels and names
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
        qsm = loadNifti(qsm_path)
        seg = loadNifti(seg_path)
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




# Generating vol and qc stats
def genVolQcStats(subjects, path):
    print('Generating volume and qc stats for' + str(len(subjects)) + 'subjects with label ')
    synthRois, values, names = synthInfo()
    vol_qsm_stats = {'total intracranial': [], 'left thalamus': [], 'left caudate': [], 'left putamen': [],  'left pallidum': [],   'left hippocampus': [],  'csf': [],
    'right thalamus':[], 'right caudate': [], 'right putamen': [], 'right pallidum': [], 'right hippocampus': []}
    vol_t1_stats = {'total intracranial': [], 'left thalamus': [], 'left caudate': [], 'left putamen': [],  'left pallidum': [],   'left hippocampus': [],  'csf': [],
    'right thalamus':[], 'right caudate': [], 'right putamen': [], 'right pallidum': [], 'right hippocampus': []}
    qc_qsm_stats = {'general white matter': [],'general grey matter': [],'general csf': [],'cerebellum':[],
    'brainstem':[],'thalamus':[],'putamen+pallidum':[],'hippocampus+amygdala':[]}
    qc_t1_stats = {'general white matter': [],'general grey matter': [],'general csf': [],'cerebellum':[],
    'brainstem':[],'thalamus':[],'putamen+pallidum':[],'hippocampus+amygdala':[]}
    # Extracting data
    for s in subjects:
        vol_qsm_path = path + s + '/qsm/vol.csv'
        qc_qsm_path = path + s + '/qsm/qc.csv'
        vol_t1_path = path + s + '/t1/vol.csv'
        qc_t1_path = path  + s + '/t1/qc.csv'
        vol_qsm = next(csv.DictReader(open(vol_qsm_path)))
        qc_qsm = next(csv.DictReader(open(qc_qsm_path)))
        vol_t1 = next(csv.DictReader(open(vol_t1_path)))
        qc_t1 = next(csv.DictReader(open(qc_t1_path)))
        for key in vol_qsm_stats:
            vol_qsm_stats[key].append(float(vol_qsm[key]))
        for key in vol_t1_stats:
            vol_t1_stats[key].append(float(vol_t1[key]))
        for key in qc_qsm_stats:
            qc_qsm_stats[key].append(float(qc_qsm[key]))
        for key in qc_t1_stats:
            qc_t1_stats[key].append(float(qc_t1[key]))
    # Generating data
    dictToExcel(vol_qsm_stats, 'vol_qsm')
    dictToExcel(vol_t1_stats, 'vol_t1')
    dictToExcel(qc_qsm_stats, 'qc_qsm')
    dictToExcel(qc_t1_stats, 'qc_t1')
    # Saving all subject data
    df_all_vol = pd.DataFrame(data=vol_qsm_stats)
    df_all_vol.to_excel('all_vol_qsm.xlsx')
    df_all_vol = pd.DataFrame(data=vol_t1_stats)
    df_all_vol.to_excel('all_vol_t1.xlsx')
    df_all_qc = pd.DataFrame(data=qc_qsm_stats)
    df_all_qc.to_excel('all_qc_qsm.xlsx')
    df_all_qc = pd.DataFrame(data=qc_t1_stats)
    df_all_qc.to_excel('all_qc_t1.xlsx')
    print('Done')




























