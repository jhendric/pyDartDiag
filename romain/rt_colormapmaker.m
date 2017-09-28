
clear all
close all


make_pal = 1;

repertoire = '/Users/romain/Work/Tools/IMEDEA/Matlab/Matlab-toolbox/Plot/';
filename = strcat(repertoire,'rt_colormaps.mat');

map = jet(100);

return


%%

if make_pal


    load(filename)

    map = rt_getcolormap(strcat(repertoire,'ncview_banded.png'),3);
    
%     titi = [62,46,35;...
%         52,28,76;...
%         25,22,54;...
%         1,52,123;...
%         7,126,208;...
%         0,80,90;...
%         0,37,36;...
%         12,87,34;...
%         112,150,10;...
%         218,189,5;...
%         214,148,8;...
%         183,39,11;...
%         43,18,15]/255;
%     N = length(titi(:,1));
%     m =10;
%     map = zeros((N-1)*m+N,3);
%     for i = 1:N-1
%         for j = 1:3
%             map((i-1)*(m+1)+1:i*(m+1)+1,j) = linspace(titi(i,j),titi(i+1,j),m+2);
%         end
%     end

    
    % Test Plot
    var = rt_ncgetvar('/Users/romain/Work/Projects/Dart/Data/NWA-RE.REANA36/Prior_Diag_20110331.nc','temp',[1,1,40,1,1],[1,1,1,-1,-1]);
%     var = rt_ncgetvar('/Data/MedClic/Data/WMED_HINDCAST/Outputs/smago_bulk/roms_avg_wmed_longterm_newmask_Y1993M01.nc','salt',[1,32,1,1],[1,1,-1,-1]);
%     rt_ncload('/akira/Romain/Projets/WMED_hindcast/Data/Outputs/smago_bulk/roms_avg_wmed_longterm_newmask_Y2000M01.nc','lon_rho','lat_rho');
    var(var==0) = NaN;
    
    fig = figure;initfigall(25,20)
    pcolor(squeeze(var));shading interp
    colormap(map)
%     colormap(rt_colormaps.charria)
    colorbar
    caxis([0 30])
    impr('/home/romain/','test',fig,'png')
    
%     
%    map2 = colormap; 
    
    % Save
    map = colormap(gca);
    rt_colormaps.paldif20 = map;
    save(filename,'rt_colormaps');

    map = rt_colormaps.charria;
    
    
    
    % map = rt_getcolormap('/home/romain/Work/matlab/cubehelix.png');
    % cb_greenwhite = colormap;
    % 
    % name_cb = whos('-file',filename);
    % save(filename,name_cb.name,'cb_greenwhite')

end






%% Plot colormaps 

load(filename)
name_cb = fieldnames(rt_colormaps);
nb_cb = length(name_cb);

resol = 200;
Z = repmat(linspace(0,1,resol),[2,1]);

fig = figure;initfigall(20,30);clf
for i = 1:nb_cb
    subplot(nb_cb,10,((i-1)*10+1):(i*10-1))
    pcolor(Z)
    shading interp
    set(gca,'XTick',[],'YTick',[])
    cmd = ['colormap(gca,rt_colormaps.',name_cb{i},')'];eval(cmd)
    subplot(nb_cb,10,i*10)
    set(gca,'Xtick',[],'Ytick',[],'Color','none','Visible','off')
    xlim([0 10])
    ylim([0 1])
    text(0,0.5,name_cb{i},'FontSize',11,'VerticalAlignment','Middle','interpreter','none')
end

toto = annotation('textbox',[0.4 0.95 0.2 0.03],'EdgeColor','none','FontSize',11,'interpreter','none',...
    'FontWeight','bold','HorizontalAlignment','center','VerticalAlignment','middle',...
    'String',['Colormaps in ' filename]);

impr_new(repertoire,'rt_colormaps',fig,'png')



%% Create colormap

% % Vert
% col(1,:) = [0 0 0];
% col(2,:) = [48 59 25]/255;
% col(3,:) = [79 98 40]/255;
% col(4,:) = [118 146 60]/255;
% col(5,:) = [158 189 95]/255;
% col(6,:) = [199 217 163]/255;
% col(7,:) = [1 1 1];
% 
% col = cb_barbara;
% 
% m = 3;
% N = length(col(:,1));
% map = zeros((N-1)*m+N,3);
% for i = 1:N-1
%     for j = 1:3
%         map((i-1)*(m+1)+1:i*(m+1)+1,j) = linspace(col(i,j),col(i+1,j),m+2);
%     end
% end
% 
% 
% 
% 
%  col = [10    24    40]/255;
% col2 = [0.0314    0.1882    0.4196];
% 
% % Rouge
% col(1,:) = [38 0 0]/255;
% col(2,:) = [200 80 70]/255;
% col(3,:) = [255 255 255]/255;
% 
% m = 50;
% N = length(col(:,1));
% map = zeros((N-1)*m+N,3);
% for i = 1:N-1
%     for j = 1:3
%         map((i-1)*(m+1)+1:i*(m+1)+1,j) = linspace(col(i,j),col(i+1,j),m+2);
%     end
% end
% map = flipud(map);
% 
% 
% colormap(map)
% 
% 
%  col = [10    24    40]/255;
% col2 = [0.0314    0.1882    0.4196];
% 
% 
% 
% % Redblue without white!
% clear col
% col(1,:) = [158 0 0]/255;
% 
% col(2,:) = [100 100 100]/255;
% 
% 
% col(3,:) = [90 175 255]/255;
% 
% 
% m = 50;
% N = length(col(:,1));
% map = zeros((N-1)*m+N,3);
% for i = 1:N-1
%     for j = 1:3
%         map((i-1)*(m+1)+1:i*(m+1)+1,j) = linspace(col(i,j),col(i+1,j),m+2);
%     end
% end
% map = flipud(map);
% 
% colormap(map)


%% Make structure

% repertoire = '/home/romain/Work/matlab/';
% filename = strcat(repertoire,'rt_colormaps.mat');
% name_cb = whos('-file',filename);
% nb_cb = size(name_cb,1);
% 
% 
% for i_cb = 1:nb_cb
%     name_tmp = name_cb(i_cb).name;
%     cmd = strcat('rt_colormaps.',name_tmp(4:end),'=',name_tmp,';');
%     eval(cmd)
% end
% 
% filename2 = strcat(repertoire,'rt_colormaps2.mat');
% save(filename2,'rt_colormaps')

%% Sort by type

load(filename)

rt_colormaps_back = rt_colormaps;
clear rt_colormaps

% One color
rt_colormaps.reds = rt_colormaps_back.reds;
rt_colormaps.greens = rt_colormaps_back.greens;
rt_colormaps.greenwhite = rt_colormaps_back.greenwhite;
rt_colormaps.blues = rt_colormaps_back.blues;
rt_colormaps.blues2 = rt_colormaps_back.blues2;
rt_colormaps.earthbrown = rt_colormaps_back.earthbrown;

% Pos/neg
rt_colormaps.redblue = rt_colormaps_back.redblue;
rt_colormaps.redblueclass = rt_colormaps_back.redblueclass;
rt_colormaps.rosevert = rt_colormaps_back.rosevert;
rt_colormaps.greenbrown = rt_colormaps_back.greenbrown;
rt_colormaps.lionel = rt_colormaps_back.lionel;
rt_colormaps.bugnylorrd = rt_colormaps_back.bugnylorrd;
rt_colormaps.spectral = rt_colormaps_back.spectral;
rt_colormaps.nasa_Moreland = rt_colormaps_back.nasa_Moreland;
rt_colormaps.paldif20 = rt_colormaps_back.paldif20;

rt_colormaps.redblue4 = rt_colormaps_back.redblue4;
rt_colormaps.fourcolors = rt_colormaps_back.fourcolors;


% Jet likes
rt_colormaps.ncview_def = rt_colormaps_back.ncview_def;
rt_colormaps.earth = rt_colormaps_back.earth;
rt_colormaps.eke1 = rt_colormaps_back.eke1;
rt_colormaps.ferret = rt_colormaps_back.ferret;
rt_colormaps.eke2 = rt_colormaps_back.eke2;
rt_colormaps.sst = rt_colormaps_back.sst;
rt_colormaps.barbara = rt_colormaps_back.barbara;
rt_colormaps.zouhair = rt_colormaps_back.zouhair;

% Lots of colors
rt_colormaps.ncview_3gauss = rt_colormaps_back.ncview_3gauss;
rt_colormaps.pastel1 = rt_colormaps_back.pastel1;
rt_colormaps.pastel2 = rt_colormaps_back.pastel2;
rt_colormaps.pastel3 = rt_colormaps_back.pastel3;
rt_colormaps.section = rt_colormaps_back.section;
rt_colormaps.section2 = rt_colormaps_back.section2;
rt_colormaps.ncview_detail = rt_colormaps_back.ncview_detail;
rt_colormaps.ifremer = rt_colormaps_back.ifremer;
rt_colormaps.testut = rt_colormaps_back.testut;
rt_colormaps.testut2 = rt_colormaps_back.testut2;
rt_colormaps.charria = rt_colormaps_back.charria;
rt_colormaps.ncview_banded = rt_colormaps_back.ncview_banded;


% Pretty
rt_colormaps.capet = rt_colormaps_back.capet;
rt_colormaps.vincent = rt_colormaps_back.vincent;
rt_colormaps.intense = rt_colormaps_back.intense;
rt_colormaps.intense2 = rt_colormaps_back.intense2;

% Weird (nasa likes)
rt_colormaps.helix = rt_colormaps_back.helix;
rt_colormaps.helix2 = rt_colormaps_back.helix2;
rt_colormaps.cubehelix = rt_colormaps_back.cubehelix;
rt_colormaps.nasa_percept1 = rt_colormaps_back.nasa_percept1;
rt_colormaps.chloro = rt_colormaps_back.chloro;
rt_colormaps.nasa_Niccoli = rt_colormaps_back.nasa_Niccoli;
rt_colormaps.accent = rt_colormaps_back.accent;

% Topos
rt_colormaps.topoland = rt_colormaps_back.topoland;
rt_colormaps.topoland2 = rt_colormaps_back.topoland2;
rt_colormaps.topoland3 = rt_colormaps_back.topoland3;
rt_colormaps.distearth = rt_colormaps_back.distearth;
rt_colormaps.toposea = rt_colormaps_back.toposea;

save(filename,'rt_colormaps');



%% Colors

clear rt_colors

rt_colors.grey      = [0.3 0.3 0.3];
rt_colors.taupe     = [122,94,72]/255;
rt_colors.brown     = [0.8 0.4 0.1];
rt_colors.flushorange    = [1 0.5 0];
rt_colors.rust      = [223,140,18]/255;
rt_colors.mantis  = [115, 206, 124]/255;
rt_colors.olive     = [123,133,18]/255;
rt_colors.killarney     = [47,95,47]/255;
rt_colors.teal      = [0,128,128]/255;
rt_colors.steel     = [0.27 0.51 0.71];
rt_colors.skyblue   = [0.50 0.55 0.95];
rt_colors.greyblue	= [99,109,158]/255;
rt_colors.margueriteblue    =[0.42 0.35 0.80];
rt_colors.hyperblue	= [0,85,157]/255;
rt_colors.navy      = [11,4,87]/255;
rt_colors.clairvoyant	= [102,9,104]/255;
rt_colors.magenta	= [177,16,92]/255;
% rt_colors.mypink    = [0.9 0.5 0.9];
rt_colors.aubergine	= [75,18,59]/255;
rt_colors.merlot	= [106,4,44]/255;
rt_colors.applered	= [152,9,11]/255;
rt_colors.burgundy  = [0.65 0.16 0.16];
rt_colors.naphthol  = [255 71 51]/255;
repertoire = '/home/romain/Work/matlab/';
filename = strcat(repertoire,'rt_colors.mat');
save(filename,'rt_colors')



%% Plot colors 


filename = strcat(repertoire,'rt_colors.mat');

load(filename)
name_c = fieldnames(rt_colors);
nb_c = length(name_c);

resol = 200;
Z = repmat(linspace(0,1,resol),[2,1]);

fig = figure;initfigall(20,30)
for i = 1:nb_c
    subplot(nb_c,10,((i-1)*10+1):(i*10-1))
    pcolor(Z)
    shading interp
    set(gca,'XTick',[],'YTick',[])
    set(gca,'Visible','off')
    cmd = ['colormap(gca,rt_colors.',name_c{i},')'];eval(cmd)
    subplot(nb_c,10,i*10)
    set(gca,'Xtick',[],'Ytick',[],'Color','none','Visible','off')
    xlim([0 10])
    ylim([0 1])
    text(0,0.5,name_c{i},'FontSize',11,'VerticalAlignment','Middle','interpreter','none')
end

toto = annotation('textbox',[0.4 0.95 0.2 0.03],'EdgeColor','none','FontSize',11,'interpreter','none',...
    'FontWeight','bold','HorizontalAlignment','center','VerticalAlignment','middle',...
    'String',['Colormaps in ' filename]);

impr_new(repertoire,'rt_colors',fig,'png','-opengl')


% Write ASCII
load(filename)
name_col = fieldnames(rt_colors);
nb_cb = length(name_col);

fileID = fopen([filename(1:end-3) 'txt'],'w');
for i =1:nb_cb
    cb_tmp = getfield(rt_colors,name_col{i});
    fprintf(fileID,'%s,%0.4f,%0.4f,%0.4f\n',name_col{i},cb_tmp);
end
fclose(fileID)



return

%% Write ASCII

load(filename)
name_cb = fieldnames(rt_colormaps);
nb_cb = length(name_cb);

fileID = fopen([filename(1:end-3) 'txt'],'w');
for i =1:nb_cb
    cb_tmp = getfield(rt_colormaps,name_cb{i});
    fprintf(fileID,[name_cb{i} '\n']);
    fprintf(fileID,'%0.8f,',cb_tmp(:,1));
    fprintf(fileID,'\n');
    fprintf(fileID,'%0.8f,',cb_tmp(:,2));
    fprintf(fileID,'\n');
    fprintf(fileID,'%0.8f,',cb_tmp(:,3));
    fprintf(fileID,'\n');
end
fclose(fileID)

return

% Test reading
fileID = fopen([filename(1:end-3) 'txt'],'r');
curr = 1;
while ~feof(fileID)
    name = fgetl(fileID);
    A = fscanf(fileID,'%f,');
    val = reshape(A,length(A)/3,[]);
    if ~exist('rt_colormaps_test','var')
        rt_colormaps_test = struct(name,val);
    else
        rt_colormaps_test = setfield(rt_colormaps_test,name,val);
    end
end
fclose(fileID)




