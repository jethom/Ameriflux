The file EC_CSAT3.EXE is a self extracting DOS file. Enclosed are two
datalogger files:  FLX231_0.CSI and FLX9K2_0.DLD. FLX231_0.CSI
is an example flux program for the CR23X datalogger and FLX9K2_0.DLD is
an example flux program for the CR9000 datalogger.

Before the program FLX231_0.CSI is downloaded to the CR23X, several unique
calibration values must be entered into the program. The station operator
must enter these unique values for five instructions. The following
multipliers must be entered:  Q7.1 positive multiplier, Q7.1 negative
multiplier, HFT3#1 multiplier, HFT3#2 multiplier, and the KH20 xKw.

Load FLX231_0.CSI into, the Campbell Scientific datalogger program editor,
EDLOG v6.0 or greater. Use the search menu to find all the occurrences
of 'unique value'. The text, unique value, is located next to each of
the locations that a unique value calibration value must be entered.

For the FLX9K2_0.DLD, the KH20's xKw must be entered.  Use PC9000 to edit the
example program FLX9K2_0.DLD.