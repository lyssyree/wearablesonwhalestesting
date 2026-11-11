plot_synthetic_data_1
savefig(gcf, 'synthetic_data_1_acceleration.fig')
exportgraphics(gcf, 'synthetic_data_1_acceleration.png', 'Resolution', 300)
repoFolder = uigetdir(pwd, 'Select tagtools_matlab-main');

if repoFolder ~= 0
    addpath(genpath(repoFolder));
end


which msa

m = msa(A, 9.81);
figure;

subplot(2,1,1)
plot(t, A)
ylabel('Acceleration (m/s^2)')
legend('X', 'Y', 'Z')
title('Original synthetic acceleration')
grid on

subplot(2,1,2)
plot(t, m)
xlabel('Time (seconds)')
ylabel('MSA (m/s^2)')
title('Animal Tags: minimum specific acceleration')
grid on

for panel = 1:2
    subplot(2,1,panel)
    for boundary = [30 60 90 120]
        xline(boundary, '--k');
    end
end


j = njerk(A, fs);
figure;

subplot(2,1,1)
plot(t, m)
ylabel('MSA (m/s^2)')
title('Animal Tags: minimum specific acceleration')
grid on

subplot(2,1,2)
plot(t, j)
xlabel('Time (seconds)')
ylabel('Norm-jerk (m/s^3)')
title('Animal Tags: norm-jerk')
grid on

for panel = 1:2
    subplot(2,1,panel)
    for boundary = [30 60 90 120]
        xline(boundary, '--k', 'HandleVisibility', 'off');
    end
end

n = round(2 * fs);

o = odba(A, n, 'wilson');
v = odba(A, n, 'vedba');
figure;

subplot(3,1,1)
plot(t, m)
ylabel('MSA (m/s^2)')
title('Minimum specific acceleration')
grid on

subplot(3,1,2)
plot(t, o)
ylabel('ODBA (m/s^2)')
title('Classic ODBA: moving-average filter')
grid on

subplot(3,1,3)
plot(t, v)
ylabel('VeDBA (m/s^2)')
xlabel('Time (seconds)')
title('VeDBA: same moving-average filter')
grid on

for panel = 1:3
    subplot(3,1,panel)
    for boundary = [30 60 90 120]
        xline(boundary, '--k', 'HandleVisibility', 'off');
    end
end
figure;
tiledlayout(5,1, 'TileSpacing', 'compact');

nexttile
plot(t, A)
ylabel('m/s^2')
title('Original acceleration')
legend('X', 'Y', 'Z')
grid on

nexttile
plot(t, m)
ylabel('m/s^2')
title('MSA')
grid on

nexttile
plot(t, j)
ylabel('m/s^3')
title('Norm-jerk')
grid on

nexttile
plot(t, o)
ylabel('m/s^2')
title('Classic ODBA')
grid on

nexttile
plot(t, v)
ylabel('m/s^2')
title('VeDBA')
xlabel('Time (seconds)')
grid on

axesList = findall(gcf, 'Type', 'axes');
for k = 1:numel(axesList)
    for boundary = [30 60 90 120]
        xline(axesList(k), boundary, '--k', ...
            'HandleVisibility', 'off');
    end
end

linkaxes(axesList, 'x');
windowSeconds = [1 2 4];
odbaWindows = zeros(size(A,1), 3);
vedbaWindows = zeros(size(A,1), 3);

for k = 1:3
    windowSamples = round(windowSeconds(k) * fs);

    odbaWindows(:,k) = odba(A, windowSamples, 'wilson');
    vedbaWindows(:,k) = odba(A, windowSamples, 'vedba');
end

figure;
tiledlayout(2,1, 'TileSpacing', 'compact');

ax1 = nexttile;
plot(t, odbaWindows)
title('ODBA: effect of moving-average window')
ylabel('ODBA (m/s^2)')
legend('1 second', '2 seconds', '4 seconds')
grid on

ax2 = nexttile;
plot(t, vedbaWindows)
title('VeDBA: effect of moving-average window')
ylabel('VeDBA (m/s^2)')
xlabel('Time (seconds)')
legend('1 second', '2 seconds', '4 seconds')
grid on

for ax = [ax1 ax2]
    for boundary = [30 60 90 120]
        xline(ax, boundary, '--k', 'HandleVisibility', 'off');
    end
end

linkaxes([ax1 ax2], 'x');
results = table(t(:), m(:), j(:), o(:), v(:), ...
    'VariableNames', {'time_s', 'MSA', 'Jerk', 'ODBA', 'VeDBA'});

writetable(results, 'matlab_results_data_1.csv');
