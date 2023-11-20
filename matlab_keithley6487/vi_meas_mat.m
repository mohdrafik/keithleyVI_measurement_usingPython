clc
close all
clear 

% Both the computer and the instrument must be configured to the same baud rate before you can successfully read or write data.
resourceList = visadevlist;
disp(resourceList)
% for me it it is printing this: Because Arduino uno is connected to my computer.
%      ResourceName     Alias     Vendor    Model    SerialNumber     Type 
%          ______________    ______    ______    _____    ____________    ______
% 
%     1    "ASRL4::INSTR"    "COM4"      ""       ""           ""         serial
% v = visadev("ASRL4::INSTR"); % connecting using Resource Name  % or  v = visadev("COM4") % --> % connecting using resource Alias
v = visadev("COM4");
disp(v)


% Reset Keithley 6487
% write(v,'*RST'); 
writeline(v,'*RST')
% Set up Keithley 6487 for voltage sourcing and current measurement
writeline(v, 'SOUR:FUNC VOLT');
writeline(v, 'SOUR:VOLT 1.0'); % Set voltage to 1.0 V
writeline(v, 'SOUR:VOLT:RANG AUTO');
writeline(v, 'SENS:FUNC "CURR"');
writeline(v, 'SENS:CURR:RANG 1e-6'); % Set current range to 1uA

% Live plot current and voltage
figure;
xlabel('Time (s)');
ylabel('Value');
title('Live Plot of Current and Voltage');

numPoints = 100;
timeInterval = 1; % in seconds

for i = 1:numPoints
    % Apply voltage
    writeline(v, 'OUTP ON');

    % Read current
    current = str2double(writeread(v, 'READ?'));

    % Plot current and voltage
    subplot(2, 1, 1);
    plot(i, current, 'ro');
    hold on;
    ylabel('Current (A)');

    subplot(2, 1, 2);
    voltage = 1.0; % Assuming a constant voltage for simplicity
    plot(i, voltage, 'bo');
    hold on;
    ylabel('Voltage (V)');

    pause(timeInterval);
end

% Turn off output and close VISA connection
writeline(v, 'OUTP OFF');
% fclose(v);
% delete(v);
clear v;