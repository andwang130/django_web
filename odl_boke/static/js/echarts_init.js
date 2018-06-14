/**
 * Created by Administrator on 2018/1/28.
 */
'use strict';
function chart_init(data) {
    var cpuChart = echarts.init(document.getElementById('cpu'));
    var memory = echarts.init(document.getElementById('memory'));
    var Harddis = echarts.init(document.getElementById('Harddis'));
    var  cpudata=data['cpu'];
    var hardata=data['Harddisk'];
    var  memodata=data['memory'];



var cpuoption = {
    color: ['#ff3d3d', '#00a0e9', '#f603ff', '#00b419', '#5f52a0'],
    legend: {
        x: 'left',
        padding: [10, 20, 0, 20],
        data: [],
    },
    tooltip: {
        alwaysShowContent: true,
        bordeRadius: 4,
        borderWidth: 1,
        borderColor: 'rgba(0,0,0,0.2)',
        backgroundColor: 'rgba(255,255,255,0.9)',
        padding: 0,
        position: "top",
        textStyle: {
            fontSize: 10,
            color: '#333'
        },
        formatter: function(params) {
            //console.log(params);
            var color = "red";
            if(parseInt(params.dataIndex) % 2 == 0){
                color = "blue";
            }
            var a = "<div style='background-color:"+color+";padding: 5px 10px;text-align:center;color:white;font-size: 20px;'>" + params.data.name[0] + "</div>";
            var num = Math.ceil(params.data.name[1].length / 10);
            a += "<div style='padding:5px;'>";
            for (var i = 0; i < num; i++) {
                a += params.data.name[1].substring(i * 10, i * 10 + 10) + "<br>";
            }
            a += "</div>";

            return a;
        }
    },
    grid: {
        left: '0',
        right: '3%',
        bottom: '3%',
        top: '13%',
        containLabel: true
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        splitLine: { //网格线
            show: true,
            lineStyle: {
                color: ['#b1b1b1'],
                type: 'dashed'
            }
        },
        data: data['times']
    },
    yAxis: {
        max: 100,
        splitLine: { //网格线
            show: true,
            lineStyle: {
                color: ['#b1b1b1'],
                type: 'dashed'
            }
        }
    },
    series: [{
        smooth: true,
        name: '',
        type: 'line',
        data: cpudata,
        label: {
            normal: {
                show: false,
                position: 'top' //值显示
            }
        }
    }]
};
var memoryoption = {
    color: ['#ff3d3d', '#00a0e9', '#f603ff', '#00b419', '#5f52a0'],
    legend: {
        x: 'left',
        padding: [10, 2, 0, 2],
        data: [],
    },
    tooltip: {
        alwaysShowContent: true,
        bordeRadius: 4,
        borderWidth: 1,
        borderColor: 'rgba(0,0,0,0.2)',
        backgroundColor: 'rgba(255,255,255,0.9)',
        padding: 0,
        position: "top",
        textStyle: {
            fontSize: 10,
            color: '#333'
        },
          formatter: function(params) {
            //console.log(params);
            var color = "red";
            if(parseInt(params.dataIndex) % 2 == 0){
                color = "blue";
            }
            var a = "<div style='background-color:"+color+";padding: 5px 10px;text-align:center;color:white;font-size: 20px;'>" + params.data.name[0] + "</div>";
            var num = Math.ceil(params.data.name[1].length / 10);
            a += "<div style='padding:5px;'>";
            for (var i = 0; i < num; i++) {
                a += params.data.name[1].substring(i * 10, i * 10 + 10) + "<br>";
            }
            a += "</div>";

            return a;
        }
    },
    grid: {
        left: '0',
        right: '3%',
        bottom: '3%',
        top: '13%',
        containLabel: true
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        splitLine: { //网格线
            show: true,
            lineStyle: {
                color: ['#b1b1b1'],
                type: 'dashed'
            }
        },
        data: data['times']
    },
    yAxis: {
        max: 100,
        splitLine: { //网格线
            show: true,
            lineStyle: {
                color: ['#b1b1b1'],
                type: 'dashed'
            }
        }
    },
    series: [{
        smooth: true,
        name: '',
        type: 'line',
        data: memodata,
        label: {
            normal: {
                show: false,
                position: 'top' //值显示
            }
        }
    }]
};
var harddisoption = {
    color: ['#ff3d3d', '#00a0e9', '#f603ff', '#00b419', '#5f52a0'],
    legend: {
        x: 'left',
        padding: [10, 20, 0, 20],
        data: [],
    },
    tooltip: {
        alwaysShowContent: true,
        bordeRadius: 60,
        borderWidth: 1,
        borderColor: 'rgba(0,0,0,0.2)',
        backgroundColor: 'rgba(255,255,255,0.9)',
        padding: 0,
        position: "top",
        textStyle: {
            fontSize: 10,
            color: '#333'
        },
          formatter: function(params) {
            //console.log(params);
            var color = "red";
            if(parseInt(params.dataIndex) % 2 == 0){
                color = "blue";
            }
            var a = "<div style='background-color:"+color+";padding: 5px 10px;text-align:center;color:white;font-size: 20px;'>" + params.data.name[0] + "</div>";
            var num = Math.ceil(params.data.name[1].length / 10);
            a += "<div style='padding:5px;'>";
            for (var i = 0; i < num; i++) {
                a += params.data.name[1].substring(i * 10, i * 10 + 10) + "<br>";
            }
            a += "</div>";

            return a;
        }
    },
    grid: {
        left: '0',
        right: '3%',
        bottom: '3%',
        top: '13%',
        containLabel: true
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        splitLine: { //网格线
            show: true,
            lineStyle: {
                color: ['#b1b1b1'],
                type: 'dashed'
            }
        },
        data: data['times']
    },
    yAxis: {
        max: 100,
        splitLine: { //网格线
            show: true,
            lineStyle: {
                color: ['#b1b1b1'],
                type: 'dashed'
            }
        }
    },
    series: [{
        smooth: true,
        name: '',
        type: 'line',
        data: hardata,
        label: {
            normal: {
                show: false,
                position: 'top' //值显示
            }
        }
    }]
};

    cpuChart.setOption(cpuoption);
    memory.setOption(memoryoption);
    Harddis.setOption(harddisoption);
}
window.onload=function () {

var serverid=$('#serverid').val()
    $.get('/server_info/get_serverinfo?serverid='+serverid, function (arg) {
        var data = JSON.parse(arg)
        chart_init(data)
    })
}