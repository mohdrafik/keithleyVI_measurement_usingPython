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
v = visadev("COM3");
disp(v)

configureTerminator(v,"CR")
% Reset Keithley 6487
% write(v,'*RST'); 
writeline(v,'*RST')

% Set up Keithley 6487 for voltage sourcing and current measurement
writeline(v, 'SOUR:FUNC VOLT');
% writeline(v, 'SOUR:VOLT 1.0'); % Set voltage to 1.0 V
writeline(v, 'SOUR:VOLT:RANG AUTO');
writeline(v, 'SENS:FUNC "CURR"');
writeline(v, 'SENS:CURR:RANG 1e-6'); % Set current range to 1uA

% Live plot current and voltage
figure;
xlabel('Time (s)');
ylabel('Value');
title('Live Plot of Current and Voltage');


v_start = 1E-3;
v_end = 10E-3;
v_step = 1E-3;
n = int(((v_end-v_start)/(v_step)) + 1);
% # print(n)
volatge_list = v_start; 
for i =2:n
    term  = v_start + (i-1)*v_step ;
%     # print(term)
    volatge_list= [volatge_list, term];
end

% numPoints = 100;
timeInterval = 1; % in seconds
[row,col] = size(volatge_list);

% for i = 1:numPoints
for i = 1:col
    % Apply voltage
    writeline(v, 'SOUR:VOLT ');
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
% end
end
% Turn off output and close VISA connection
writeline(v, 'OUTP OFF');
% fclose(v);
% delete(v);
clear v;