%% Function Test
clear all;
close all;
clc;

format long;

% x = [x1,x2,x3,x4]
x = [0.30,
    0.20,
    0.015,
    0.015];

[y] = ibeam_nrf_out(x);

ibeam_nrf_out_display;
