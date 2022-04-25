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
* Initial object 
* Initial probe 
    * real space on specimen before any update
    * Fourier space on specimen before any update
* Exit wave before FFT
* Exit wave after FFT (far-field)
* Intensity (predicted CBED)
* Partial derivative of the potential
