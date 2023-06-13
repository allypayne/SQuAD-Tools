# Guidelines to Creating and Understanding Werk SQuAD Plots
## Here I'll give you an introduction to understanding the plots that we create and the tools to create your own!

# Plots for the Poster
If you want to create a draft plot with our data you can do so with the make_plot function within my script titled "detections"
You should first create a data set using "detections" for either the HI or OVI the detections and another data set for the OVI detections. You will then need to create a "non detections" data set using the same script file. This are both required parameters for the make_plot function. With these tools you can create draft plots that we are using in our upcoming poster!
Start by adjusting the color bar (and corresponding titles); ideas for these plots include: sqrt_M_tot_OVI, sqrt_M_tot_HI, H_I_total_log10_N, O_VI_total_log10_N

## Understanding Detections
These are defined as galaxies that meet all of our selection criteria and show absorption features in the QSO spectrum for gas within it's circumgalactic medium. To classify as a true detection within our analysis the component must have a correponding detection threshold of <= 13.5 (anything higher will allow for too much noise within our data to confidently say this absorption feature has been detected within the CGM and wont allow us to extract reliable absoprtion data).

## Understanding Non Detections
They are defined as the galaxies that meet all of our selection criteria but there are no absorption features detected for the galaxy (or the features are not strong enought...). In our large compiled data set these can be found under the columns, "N_H_I_components" or "N_O_VI_components" (number of H I or O VI components). These will have values of zero for a non detection. (Note: There are galaxies that will have zero O VI components but will still have H I detections and vice versa).

My code refers to a basic and a safe non detection.
For our analysis we are playing it safe to increase our certainty (hence, the **safe** non detections). A safe non detection means it has no components with absorption features (has a value of zero for N_H_I_components or N_O_VI_components) AND it the associated column density from its absorption feature is less than the detection threshold corresponding to this galaxy. This means that the absorption feature was not strong enough to be confidently considered a component and not a noisy signal.

A **basic** non detection is only defined as a galaxy that has no associated components for a given ion.
