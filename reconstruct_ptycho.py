from ptychography import reconstruct_ptychography
import numpy as np
import dxchange
import datetime
import argparse
import os

timestr = str(datetime.datetime.today())
timestr = timestr[:timestr.find('.')]
for i in [':', '-', ' ']:
    if i == ' ':
        timestr = timestr.replace(i, '_')
    else:
        timestr = timestr.replace(i, '')

parser = argparse.ArgumentParser()
parser.add_argument('--epoch', default='None')
parser.add_argument('--save_path', default='cone_256_foam_ptycho')
parser.add_argument('--output_folder', default='test') # Will create epoch folders under this
args = parser.parse_args()
epoch = args.epoch
if epoch == 'None':
    epoch = 0
    init = None
else:
    epoch = int(epoch)
    if epoch == 0:
        init = None
    else:
        init_delta = dxchange.read_tiff(os.path.join(args.save_path, args.output_folder, 'epoch_{}/delta_ds_1.tiff'.format(epoch - 1)))
        init_beta = dxchange.read_tiff(os.path.join(args.save_path, args.output_folder, 'epoch_{}/beta_ds_1.tiff'.format(epoch - 1)))
        print(os.path.join(args.save_path, args.output_folder, 'epoch_{}/delta_ds_1.tiff'.format(epoch - 1)))
        init = [np.array(init_delta[...]), np.array(init_beta[...])]


params_adhesin_2 = {'fname': 'data_adhesin_64_1nm_1um.h5',
                  'theta_st': 0,
                  'theta_end': 2 * np.pi,
                  'theta_downsample': None,
                  'n_epochs': 10,
                  'obj_size': (64, 64, 64),
                  'alpha_d': 0,
                  'alpha_b': 0,
                  'gamma': 0,
                  'probe_size': (72, 72),
                  # 'learning_rate': 1e-7, # for non-shared file mode
                  'learning_rate': 1e-8, # for shared-file mode
                  'center': 32,
                  'energy_ev': 800,
                  'psize_cm': 0.67e-7,
                  'minibatch_size': 23,
                  'n_batch_per_update': 1,
                  'output_folder': 'test_bilinear',
                  'cpu_only': True,
                  'save_path': 'adhesin_ptycho_2',
                  'multiscale_level': 1,
                  'n_epoch_final_pass': None,
                  'save_intermediate': True,
                  'full_intermediate': True,
                  # 'initial_guess': [np.load('adhesin_ptycho_2/phantom/grid_delta.npy'), np.load('adhesin_ptycho_2/phantom/grid_beta.npy')],
                  'initial_guess': None,
                  # 'probe_initial': [dxchange.read_tiff('adhesin_ptycho_2/probe_mag_defocus_10nm.tiff'), dxchange.read_tiff('adhesin_ptycho_2/probe_phase_defocus_10nm.tiff')],
                  'probe_initial': None,
                  'n_dp_batch': 529,
                  'fresnel_approx': True,
                  'probe_type': 'gaussian',
                  'probe_learning_rate': 1e-3,
                  'probe_learning_rate_init': 1e-3,
                  'finite_support_mask': None,
                  'forward_algorithm': 'fresnel',
                  'object_type': 'normal',
                  'probe_pos': [(y, x) for y in np.linspace(9, 55, 23, dtype=int) for x in np.linspace(9, 55, 23, dtype=int)],
                  'probe_mag_sigma': 6,
                  'probe_phase_sigma': 6,
                  'probe_phase_max': 0.5,
                  'optimize_probe_defocusing': False,
                  'probe_defocusing_learning_rate': 1e-7,
                  'shared_file_object': True
                  }

params_cone_marc = {'fname': 'data_cone_256_foam_1nm.h5',
                    'theta_st': 0,
                    'theta_end': 2 * np.pi,
                    'theta_downsample': None,
                    'n_epochs': 1,
                    'obj_size': (256, 256, 256),
                    'alpha_d': 1e-9 * 1.7e7,
                    'alpha_b': 1e-10 * 1.7e7,
                    'gamma': 1e-9 * 1.7e7,
                    'probe_size': (72, 72),
                    'learning_rate': 5e-7,
                    'center': 128,
                    'energy_ev': 5000,
                    'psize_cm': 1.e-7,
                    'minibatch_size': 23,
                    'n_batch_per_update': 1,
                    # 'output_folder': 'theta_' + timestr,
                    'output_folder': os.path.join(args.output_folder, 'epoch_{}'.format(epoch)),
                    'cpu_only': True,
                    'save_path': 'cone_256_foam_ptycho',
                    'multiscale_level': 1,
                    'n_epoch_final_pass': None,
                    'save_intermediate': True,
                    'full_intermediate': True,
                    'initial_guess': init,
                    'n_dp_batch': 23,
                    'probe_type': 'gaussian',
                    'forward_algorithm': 'fresnel',
                    'probe_pos': [(y, x) for y in np.arange(23) * 12 for x in np.arange(23) * 12],
                    'finite_support_mask': None,
                    'probe_mag_sigma': 6,
                    'probe_phase_sigma': 6,
                    'probe_phase_max': 0.5,
                    'shared_file_object': False,
                    'reweighted_l1': False if epoch == 0 else True,
                    }

# params_cone_marc = {'fname': 'data_cone_256_1nm_marc.h5',
#                     'theta_st': 0,
#                     'theta_end': 2 * np.pi,
#                     'theta_downsample': 5,
#                     'n_epochs': 5,
#                     'obj_size': (256, 256, 256),
#                     'alpha_d': 0,
#                     'alpha_b': 0,
#                     'gamma': 0,
#                     'probe_size': (72, 72),
#                     'learning_rate': 1e-9,
#                     'center': 128,
#                     'energy_ev': 5000,
#                     'psize_cm': 1.e-7,
#                     'minibatch_size': 1,
#                     'n_batch_per_update': 1,
#                     'output_folder': 'test',
#                     'cpu_only': True,
#                     'save_path': 'cone_256_filled_ptycho',
#                     'phantom_path': 'cone_256_filled_ptycho/phantom',
#                     'multiscale_level': 1,
#                     'n_epoch_final_pass': None,
#                     'save_intermediate': True,
#                     'full_intermediate': True,
#                     'initial_guess': None,
#                     'n_dp_batch': 20,
#                     'probe_type': 'gaussian',
#                     'forward_algorithm': 'fresnel',
#                     'probe_pos': [(y, x) for y in np.arange(23) * 12 for x in np.arange(23) * 12],
#                     'finite_support_mask': None,
#                     'probe_mag_sigma': 6,
#                     'probe_phase_sigma': 6,
#                     'probe_phase_max': 0.5,
#                     }

params_2d = {'fname': 'data_cone_256_1nm_marc.h5',
                    'theta_st': 0,
                    'theta_end': 0,
                    'theta_downsample': 1,
                    'n_epochs': 500,
                    'obj_size': (256, 256, 1),
                    'alpha_d': 0,
                    'alpha_b': 0,
                    'gamma': 5e-11,
                    'probe_size': (72, 72),
                    'learning_rate': 1e-6,
                    'center': 128,
                    'energy_ev': 5000,
                    'psize_cm': 1.e-7,
                    'minibatch_size': 1,
                    'n_batch_per_update': 1,
                    'output_folder': 'ptycho/test',
                    'cpu_only': True,
                    'save_path': '2d',
                    'multiscale_level': 1,
                    'n_epoch_final_pass': None,
                    'save_intermediate': True,
                    'full_intermediate': True,
                    'initial_guess': None,
                    'n_dp_batch': 20,
                    'probe_type': 'gaussian',
                    'probe_options': {'probe_mag_sigma': 6,
                                      'probe_phase_sigma': 6,
                                      'probe_phase_max': 0.5},
                    'forward_algorithm': 'fresnel',
                    'probe_pos': [(y, x) for y in np.arange(23) * 12 for x in np.arange(23) * 12],
                    'finite_support_mask': None,
                    'object_type': 'normal',
                    }

params_2d_cell = {'fname': 'data_cell_phase_n1e9_ref.h5',
                    'theta_st': 0,
                    'theta_end': 0,
                    'theta_downsample': 1,
                    'n_epochs': 200,
                    'obj_size': (325, 325, 1),
                    'alpha_d': 0,
                    'alpha_b': 0,
                    'gamma': 0,
                    'probe_size': (72, 72),
                    'learning_rate': 4e-3,
                    'center': 512,
                    'energy_ev': 5000,
                    'psize_cm': 1.e-7,
                    'minibatch_size': 1,
                    'n_batch_per_update': 1,
                    'output_folder': 'n1e9_ref',
                    'cpu_only': True,
                    'save_path': 'cell/ptychography',
                    'multiscale_level': 1,
                    'n_epoch_final_pass': None,
                    'save_intermediate': True,
                    'full_intermediate': True,
                    # 'initial_guess': [np.zeros([325, 325, 1]) + 0.032, np.zeros([325, 325, 1])],
                    'initial_guess': None,
                    'n_dp_batch': 20,
                    'probe_type': 'gaussian',
                    'probe_options': {'probe_mag_sigma': 6,
                                      'probe_phase_sigma': 6,
                                      'probe_phase_max': 0.5},
                    'forward_algorithm': 'fresnel',
                    'object_type': 'phase_only',
                    'probe_pos': [(y, x) for y in np.arange(33) * 10 for x in np.arange(34) * 10],
                    'finite_support_mask': None
                    }

params_cone_marc_noisy = {'fname': 'data_cone_256_1nm_marc_n2e5.h5',
                          'theta_st': 0,
                          'theta_end': 2 * np.pi,
                          'theta_downsample': None,
                          'n_epochs': 1,
                          'obj_size': (256, 256, 256),
                          'alpha_d': 1e-9,
                          'alpha_b': 1e-10,
                          'gamma': 1e-9,
                          'probe_size': (72, 72),
                          'learning_rate': 1e-7,
                          'center': 128,
                          'energy_ev': 5000,
                          'psize_cm': 1.e-7,
                          'minibatch_size': 1,
                          'n_batch_per_update': 1,
                          'output_folder': 'n2e5/xrmlite_iter3',
                          'cpu_only': True,
                          'save_path': 'cone_256_filled_ptycho',
                          'multiscale_level': 1,
                          'n_epoch_final_pass': None,
                          'save_intermediate': True,
                          'full_intermediate': True,
                          'initial_guess': init,
                          'n_dp_batch': 20,
                          'probe_type': 'gaussian',
                          'probe_options': {'probe_mag_sigma': 6,
                                            'probe_phase_sigma': 6,
                                            'probe_phase_max': 0.5},
                          'forward_algorithm': 'fresnel',
                          'probe_pos': [(y, x) for y in np.arange(23) * 12 for x in np.arange(23) * 12],
                          'finite_support_mask': None
                          }

params_cone = {'fname': 'data_cone_256_1nm_marc.h5',
               'theta_st': 0,
               'theta_end': 2 * np.pi,
               'n_epochs': 1,
               'obj_size': (256, 256, 256),
               'alpha_d': 0,
               'alpha_b': 0,
               'gamma': 0,
               'probe_size': (72, 72),
               'learning_rate': 1e-7,
               'center': 128,
               'energy_ev': 5000,
               'psize_cm': 1.e-7,
               'minibatch_size': 1,
               'n_batch_per_update': 1,
               'output_folder': 'test',
               'cpu_only': True,
               'save_path': 'cone_256_filled_ptycho',
               'multiscale_level': 1,
               'n_epoch_final_pass': None,
               'save_intermediate': True,
               'full_intermediate': True,
               'initial_guess': None,
               'n_dp_batch': 100,
               'probe_type': 'gaussian',
               'probe_options': {'probe_mag_sigma': 6,
                                 'probe_phase_sigma': 6,
                                 'probe_phase_max': 0.5},
               'forward_algorithm': 'fd',
               # 'probe_pos': [(y, x) for y in np.linspace(18, 120, 35, dtype=int) for x in np.linspace(54, 198, 49, dtype=int)] +
               #              [(y, x) for y in np.linspace(120, 222, 35, dtype=int) for x in np.linspace(22, 230, 70, dtype=int)],
               'probe_pos': [(y, x) for y in np.arange(23) * 12 for x in np.arange(23) * 12],
               'finite_support_mask': dxchange.read_tiff('cone_256_filled_ptycho/mask.tiff')
               }

params = params_adhesin_2
# params = params_cone_marc
# params = params_2d_cell


# reconstruct_ptychography(fname=params['fname'],
#                          probe_pos=params['probe_pos'],
#                          probe_size=params['probe_size'],
#                          theta_st=0,
#                          theta_end=params['theta_end'],
#                          theta_downsample=params['theta_downsample'],
#                          obj_size=params['obj_size'],
#                          n_epochs=params['n_epochs'],
#                          crit_conv_rate=0.03,
#                          max_nepochs=200,
#                          alpha_d=params['alpha_d'],
#                          alpha_b=params['alpha_b'],
#                          gamma=params['gamma'],
#                          learning_rate=params['learning_rate'],
#                          output_folder=params['output_folder'],
#                          minibatch_size=params['minibatch_size'],
#                          save_intermediate=params['save_intermediate'],
#                          full_intermediate=params['full_intermediate'],
#                          energy_ev=params['energy_ev'],
#                          psize_cm=params['psize_cm'],
#                          cpu_only=params['cpu_only'],
#                          save_path=params['save_path'],
#                          phantom_path=params['phantom_path'],
#                          multiscale_level=params['multiscale_level'],
#                          n_epoch_final_pass=params['n_epoch_final_pass'],
#                          initial_guess=params['initial_guess'],
#                          n_batch_per_update=params['n_batch_per_update'],
#                          dynamic_rate=True,
#                          probe_type=params['probe_type'],
#                          probe_initial=None,
#                          probe_learning_rate=1e-3,
#                          pupil_function=None,
#                          probe_circ_mask=None,
#                          n_dp_batch=params['n_dp_batch'],
#                          finite_support_mask=params['finite_support_mask'],
#                          forward_algorithm=params['forward_algorithm'],
#                          object_type=params['object_type'],
#                          fresnel_approx=params['fresnel_approx'],
#                          **params['probe_options'])

# reconstruct_ptychography_hdf5(fname=params['fname'],
#                               probe_pos=params['probe_pos'],
#                               probe_size=params['probe_size'],
#                               theta_st=0,
#                               theta_end=params['theta_end'],
#                               theta_downsample=params['theta_downsample'],
#                               obj_size=params['obj_size'],
#                               n_epochs=params['n_epochs'],
#                               crit_conv_rate=0.03,
#                               max_nepochs=200,
#                               alpha_d=params['alpha_d'],
#                               alpha_b=params['alpha_b'],
#                               gamma=params['gamma'],
#                               learning_rate=params['learning_rate'],
#                               output_folder=params['output_folder'],
#                               minibatch_size=params['minibatch_size'],
#                               save_intermediate=params['save_intermediate'],
#                               full_intermediate=params['full_intermediate'],
#                               energy_ev=params['energy_ev'],
#                               psize_cm=params['psize_cm'],
#                               cpu_only=params['cpu_only'],
#                               save_path=params['save_path'],
#                               phantom_path=params['phantom_path'],
#                               multiscale_level=params['multiscale_level'],
#                               n_epoch_final_pass=params['n_epoch_final_pass'],
#                               initial_guess=params['initial_guess'],
#                               n_batch_per_update=params['n_batch_per_update'],
#                               dynamic_rate=True,
#                               probe_type=params['probe_type'],
#                               probe_initial=None,
#                               probe_learning_rate=params['probe_learning_rate'],
#                               probe_learning_rate_init=params['probe_learning_rate_init'],
#                               pupil_function=None,
#                               probe_circ_mask=None,
#                               n_dp_batch=params['n_dp_batch'],
#                               finite_support_mask=params['finite_support_mask'],
#                               forward_algorithm=params['forward_algorithm'],
#                               object_type=params['object_type'],
#                               fresnel_approx=params['fresnel_approx'],
#                               **params['probe_options'])

# reconstruct_ptychography_hdf5(**params)
reconstruct_ptychography(**params)
