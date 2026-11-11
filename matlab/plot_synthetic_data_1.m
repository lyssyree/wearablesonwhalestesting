% Select synthetic_accelerometer_1.csv when prompted.
[file, folder] = uigetfile('*.csv', 'Select synthetic_accelerometer_1.csv');
if isequal(file, 0)
    return
end
T = readtable(fullfile(folder, file));
t = T.time_s;
A = [T.ax_m_s2 T.ay_m_s2 T.az_m_s2];
fs = 1 / median(diff(t));
figure;
plot(t, A);
xlabel('Time (s)'); ylabel('Acceleration (m/s^2)');
legend('X','Y','Z'); title('Synthetic accelerometer data 1');
grid on;
for boundary = [30 60 90 120]
    xline(boundary, '--k');
end
% A is the N-by-3 acceleration matrix for Animal Tags functions.
% fs is the sampling rate in Hz. Labels are in T.condition.
% Example after installing Animal Tags: m = msa(A, 9.81);
