# TODO

1. Change cm -> nm
2. Support complex number operations
3. Compare initial probe function from ROP to what Adorym gets from ifft
4. Add initial probe generation from parameters.
5. Is the normalization in `propagate.py:285` the source of the differences in magnitude? 

# Notes

* `this_pred_batch` is raw data magnitudes (sqrt)
* Fresnel propagator is the same.
* `repeating_slice` is similar to equal slices?
* The argument for `update_scheme` has been changed to `per_angle` from `per angle`.
* ROP comparison was done with L1 and 30 slices... 
* The loss is computed with magnitudes, not intensities `forward_model.py:106`

# Comparison
## Initial Conditions
* L2 Norm
* Learning rate = `.00078125`
* conjugate gradient - only update object (epoch == sub-epoch)
* same input probe (128x128)
    * Marcel crops probe, and updates probe positions
* same input probe (272x272)
    * Tom pads CBEDs with 0s, probe positions remain the same

## Arrays to compare
* Initial object - `initial_obj.npy` - `[200,200,1,2]`
* Fresnel kernel propagator - `fresnel_kernel.npy` - `[128, 128]`
* Initial probe 
    * real space on specimen before any update - `probe_real.npy, probe_imag.npy` - `[1, 128, 128]`
    * Fourier space on specimen before any update - `probe_fft_real.npy, probe_fft_imag.npy` - `[128, 128]` - these have been manually fft2 and fftshifted using numpy. Care for numpy fft scaling!!
* Exit wave before FFT - `exit_wave_beforefft_real.npy, exit_wave_beforefft_imag.numpy` - `[120, 128, 128]` - first 120 positions
* Exit wave after FFT (far-field)- `exit_wave_afterfft_real.npy, exit_wave_afterfft_imag.numpy` - `[120, 128, 128]` - first 120 positions
* Intensity (predicted CBED) - `exit_cbed_mag.npy` - `[120, 128, 128]` - first 120 positions _magnitude_. Adorym computes error on the basis of *magnitude*. 
* Partial derivative of the potential / gradient? 
     - after first batch of 120 patterns - `gradient_batch0.npy` - `[248, 248, 1, 2]`
     - whole object iteration - `gradient_epoch0.npy` - `[248, 248, 1, 2]`