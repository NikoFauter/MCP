EESchema Schematic File Version 4
LIBS:RPi_Hat-cache
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 2
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L RPi_Hat-rescue:RPi_GPIO-RPi_Hat-rescue J2
U 1 1 5516AE26
P 7500 2700
AR Path="/5516AE26" Ref="J2"  Part="1" 
AR Path="/5515D395/5516AE26" Ref="J2"  Part="1" 
F 0 "J2" H 8250 2950 60  0000 C CNN
F 1 "RPi_GPIO" H 8250 2850 60  0000 C CNN
F 2 "RPi_Hat:Pin_Header_Straight_2x20" H 7500 2700 60  0001 C CNN
F 3 "" H 7500 2700 60  0000 C CNN
	1    7500 2700
	1    0    0    -1  
$EndComp
Text Notes 7800 5000 0    60   Italic 0
Thru-Hole Connector
$Comp
L Device:LED D1
U 1 1 5E491DEE
P 6600 2850
F 0 "D1" V 6639 2733 50  0000 R CNN
F 1 "LED" V 6548 2733 50  0000 R CNN
F 2 "LED_SMD:LED_0805_2012Metric" H 6600 2850 50  0001 C CNN
F 3 "~" H 6600 2850 50  0001 C CNN
	1    6600 2850
	0    -1   -1   0   
$EndComp
Wire Wire Line
	7300 2700 6600 2700
$Comp
L Device:R R1
U 1 1 5E4949FF
P 6600 3250
F 0 "R1" H 6670 3296 50  0000 L CNN
F 1 "R" H 6670 3205 50  0000 L CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 6530 3250 50  0001 C CNN
F 3 "~" H 6600 3250 50  0001 C CNN
	1    6600 3250
	1    0    0    -1  
$EndComp
Wire Wire Line
	6600 3000 6600 3100
Wire Wire Line
	6600 3400 6600 3900
Wire Wire Line
	6600 3900 7300 3900
$EndSCHEMATC
