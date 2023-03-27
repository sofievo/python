#!/usr/bin/env pyhton3

import numpy as np
import nibabel as nib


def rescaleNifti(path, name):
    dicom_values = nib.load(path)
    data = dicom_values.get_fdata()
    print('Rescaling ', path, ' from dicom to nifti values \nInput min-max: '+ str(np.round(np.min(data),5))+ '-', np.round(np.max(data),5))
    data_res = data/10000 -0.2048
    data_res[data_res > 0.2047] = 0.2047
    data_res[data_res < -0.2048] = -0.2048
    nifti_values = nib.Nifti1Image(data_res, dicom_values.affine, dicom_values.header)
    nib.save(nifti_values, name + '.nii.gz')
    print('Output min-max: ', np.round(np.min(data_res),5), '-', np.round(np.max(data_res),5) )
    return nifti_values


n = rescaleNifti("/mnt/work/users/sofievor/segments_cQSM_T1/P7T_008F032/qsm/qsm.nii.gz", 'qsmF032')
n = rescaleNifti("/mnt/work/users/sofievor/segments_cQSM_T1/P7T_008F033/qsm/qsm.nii.gz", 'qsmF033')
n = rescaleNifti("/mnt/work/users/sofievor/segments_cQSM_T1/P7T_008F034/qsm/qsm.nii.gz", 'qsmF034')
n = rescaleNifti("/mnt/work/users/sofievor/segments_cQSM_T1/P7T_008F035/qsm/qsm.nii.gz", 'qsmF035')
n = rescaleNifti("/mnt/work/users/sofievor/segments_cQSM_T1/P7T_008F036/qsm/qsm.nii.gz", 'qsmF036')
n = rescaleNifti("/mnt/work/users/sofievor/segments_cQSM_T1/P7T_008F038/qsm/qsm.nii.gz", 'qsmF038')


