var theme = {
  color: [
    '#26B99A', '#34495E', '#BDC3C7', '#3498DB',
    '#9B59B6', '#8abb6f', '#759c6a', '#bfd3b7'
  ],

  title: {
    itemGap: 8,
    textStyle: {
      fontWeight: 'normal',
      color: '#408829'
    }
  },

  dataRange: {
    color: ['#1f610a', '#97b58d']
  },

  toolbox: {
    color: ['#408829', '#408829', '#408829', '#408829']
  },

  tooltip: {
    backgroundColor: 'rgba(0,0,0,0.5)',
    axisPointer: {
      type: 'line',
      lineStyle: {
        color: '#408829',
        type: 'dashed'
      },
      crossStyle: {
        color: '#408829'
      },
      shadowStyle: {
        color: 'rgba(200,200,200,0.3)'
      }
    }
  },

  dataZoom: {
    dataBackgroundColor: '#eee',
    fillerColor: 'rgba(64,136,41,0.2)',
    handleColor: '#408829'
  },
  grid: {
    borderWidth: 0
  },

  categoryAxis: {
    axisLine: {
      lineStyle: {
        color: '#408829'
      }
    },
    splitLine: {
      lineStyle: {
        color: ['#eee']
      }
    }
  },

  valueAxis: {
    axisLine: {
      lineStyle: {
        color: '#408829'
      }
    },
    splitArea: {
      show: true,
      areaStyle: {
        color: ['rgba(250,250,250,0.1)', 'rgba(200,200,200,0.1)']
      }
    },
    splitLine: {
      lineStyle: {
        color: ['#eee']
      }
    }
  },
  timeline: {
    lineStyle: {
      color: '#408829'
    },
    controlStyle: {
      normal: {color: '#408829'},
      emphasis: {color: '#408829'}
    }
  },

  k: {
    itemStyle: {
      normal: {
        color: '#68a54a',
        color0: '#a9cba2',
        lineStyle: {
          width: 1,
          color: '#408829',
          color0: '#86b379'
        }
      }
    }
  },
  map: {
    itemStyle: {
      normal: {
        areaStyle: {
          color: '#ddd'
        },
        label: {
          textStyle: {
            color: '#c12e34'
          }
        }
      },
      emphasis: {
        areaStyle: {
          color: '#99d2dd'
        },
        label: {
          textStyle: {
            color: '#c12e34'
          }
        }
      }
    }
  },
  force: {
    itemStyle: {
      normal: {
        linkStyle: {
          strokeColor: '#408829'
        }
      }
    }
  },
  chord: {
    padding: 4,
    itemStyle: {
      normal: {
        lineStyle: {
          width: 1,
          color: 'rgba(128, 128, 128, 0.5)'
        },
        chordStyle: {
          lineStyle: {
            width: 1,
            color: 'rgba(128, 128, 128, 0.5)'
          }
        }
      },
      emphasis: {
        lineStyle: {
          width: 1,
          color: 'rgba(128, 128, 128, 0.5)'
        },
        chordStyle: {
          lineStyle: {
            width: 1,
            color: 'rgba(128, 128, 128, 0.5)'
          }
        }
      }
    }
  },
  gauge: {
    startAngle: 225,
    endAngle: -45,
    axisLine: {
      show: true,
      lineStyle: {
        color: [[0.2, '#86b379'], [0.8, '#68a54a'], [1, '#408829']],
        width: 8
      }
    },
    axisTick: {
      splitNumber: 10,
      length: 12,
      lineStyle: {
        color: 'auto'
      }
    },
    axisLabel: {
      textStyle: {
        color: 'auto'
      }
    },
    splitLine: {
      length: 18,
      lineStyle: {
        color: 'auto'
      }
    },
    pointer: {
      length: '90%',
      color: 'auto'
    },
    title: {
      textStyle: {
        color: '#333'
      }
    },
    detail: {
      textStyle: {
        color: 'auto'
      }
    }
  },
  textStyle: {
    fontFamily: 'Arial, Verdana, sans-serif'
  }
};

var option2 = {
                title: {
                  text: 'Hello',
                  subtext: 'Subtitle'
                }
            };
var stocksData;
var dateRange = {
  from_time : "2015-01-02",
  to_time : "2016-02-02"
}

function date_format(date){
  dateSet = date.split('/');
  result = dateSet[2] + '-' + dateSet[0] + '-'+ dateSet[1];
  return result;
}

function get_date(date_str){
  date_item = date_str.split(' - ');
  result = {};
  result['from_time'] = date_format(date_item[0]);
  result['to_time'] = date_format(date_item[1]);
  return result;
}



function checkBoxClick(){
  var checkedBound = [];
  var lowestBound = 0;
  $.each($("#priceTable input"), function(i,item){
    if(item.checked){
      checkedBound.push(i);
      if((stocksData.data[i][stocksData.colName[3]]) < lowestBound || lowestBound==0){
        lowestBound = stocksData.data[i][stocksData.colName[3]];
      }
    }
  });
  $('#priceTable').html("");
  $.each(stocksData.data, function(i,item){
    if ((stocksData.data[i][stocksData.colName[3]]) >= lowestBound){
      var attrItem;
      if (checkedBound.indexOf(i)==-1){
        attrItem = {
                type: "checkbox",
                id: "check-all",
                class: "flat",
                onclick: "checkBoxClick()"
              };
      }
      else{
        attrItem = {
                type: "checkbox",
                id: "check-all",
                class: "flat",
                onclick: "checkBoxClick()",
                checked: true
              };
      }
      $('#priceTable').append(
          $('<tr>').append(
            $('<td>').append(
              $('<input>').attr(attrItem)),
            $('<td>').append(stocksData.data[i][stocksData.colName[6]]),
            $('<td>').append(stocksData.data[i][stocksData.colName[0]]),
            $('<td>').append(stocksData.data[i][stocksData.colName[1]]),
            $('<td>').append(stocksData.data[i][stocksData.colName[2]]),
            $('<td>').append(stocksData.data[i][stocksData.colName[3]]),
            $('<td>').append(stocksData.data[i][stocksData.colName[4]]),
            $('<td>').append(stocksData.data[i][stocksData.colName[5]])
            ));
    }
  });
  $('#stocksTable').DataTable();
}

//update sma charts
function update_sma(){
  var urlPrice = "backend/get_moving_avg";
    var input = {'ticker': getUrlParameter('ticker'),'time_type': 'historical', 'from_time': dateRange.from_time,'to_time':dateRange.to_time};
    console.log(input);
    if (input === undefined){
        var input = {'ticker': 'AMZN'};
    }
     $.ajax({type: "post",
        url: urlPrice,
        data: input,
        dataType: 'json',
        success: function(data){
            console.log(data)
            //update echart
            var echartLine = echarts.init(document.getElementById('SMA_chart'), theme);
            echartLine.setOption({
                title: {
                  text: getUrlParameter('ticker'),
                  subtext: 'Line Chart'
                },
                tooltip: {
                  trigger: 'axis'
                },
                legend: {
                  x: 220,
                  y: 40,
                  data: ['price','SMA1','SMA2']
                },
                toolbox: {
                  show: true,
                  feature: {
                    magicType: {
                      show: true,
                      title: {
                        line: 'Line',
                        bar: 'Bar',
                        stack: 'Stack',
                        tiled: 'Tiled'
                      },
                      type: ['line', 'bar', 'stack', 'tiled']
                    },
                    restore: {
                      show: true,
                      title: "Restore"
                    },
                    saveAsImage: {
                      show: true,
                      title: "Save Image"
                    }
                  }
                },
                calculable: true,
                xAxis: [{
                  type: 'category',
                  boundaryGap: false,
                  data: data.date
                }],
                yAxis: [{
                  type: 'value'
                }],
                series: [{
                  name: 'price',
                  type: 'line',
                  smooth: true,
                  itemStyle: {

                  },
                  data: data.prices
                }, {
                  name: 'SMA1',
                  type: 'line',
                  smooth: true,
                  itemStyle: {
                    emphasis:{
                      lineStyle:{
                        type: 'dotted'
                      }
                    }
                  },
                  data: data.SMA1
                }, {
                  name: 'SMA2',
                  type: 'line',
                  smooth: true,
                  itemStyle: {
                    emphasis:{
                      lineStyle:{
                        type: 'dashed'
                      }
                    }
                  },
                  data: data.SMA2
                }]
              });
            },
        fail: function(){
            console.log('query fail.');
          }
        });
}

//update rsi
function update_rsi(){
  var urlPrice = "backend/get_rsi";
    var input = {'ticker': getUrlParameter('ticker'),'time_type': 'historical', 'from_time': dateRange.from_time,'to_time':dateRange.to_time};
    console.log(input);
    if (input === undefined){
        var input = {'ticker': 'AMZN'};
    }
     $.ajax({type: "post",
        url: urlPrice,
        data: input,
        dataType: 'json',
        success: function(data){
            console.log(data)
            //update echart
            var echartLine = echarts.init(document.getElementById('RSI_chart'), theme);
            echartLine.setOption({
                title: {
                  text: getUrlParameter('ticker'),
                  subtext: 'Line Chart'
                },
                tooltip: {
                  trigger: 'axis'
                },
                legend: {
                  x: 220,
                  y: 40,
                  data: ['rsi']
                },
                toolbox: {
                  show: true,
                  feature: {
                    magicType: {
                      show: true,
                      title: {
                        line: 'Line',
                        bar: 'Bar',
                        stack: 'Stack',
                        tiled: 'Tiled'
                      },
                      type: ['line', 'bar', 'stack', 'tiled']
                    },
                    restore: {
                      show: true,
                      title: "Restore"
                    },
                    saveAsImage: {
                      show: true,
                      title: "Save Image"
                    }
                  }
                },
                calculable: true,
                xAxis: [{
                  type: 'category',
                  boundaryGap: false,
                  data: data.date
                }],
                yAxis: [{
                  type: 'value'
                }],
                series: [{
                  name: 'rsi',
                  type: 'line',
                  smooth: true,
                  itemStyle: {

                  },
                  data: data.rsi,
                  markLine: {
                      data: [
                          {yAxis: 20},
                          {yAxis: 80}
                      ]
                  }
                }]
              });
            },
        fail: function(){
            console.log('query fail.');
          }
        });
}

//update macd chart 
function update_macd(){
  var urlPrice = "backend/get_macd";

    var input = {'ticker': getUrlParameter('ticker'),'time_type': 'historical', 'from_time': dateRange.from_time,'to_time':dateRange.to_time};
    console.log(input);
    if (input === undefined){
        var input = {'ticker': 'AMZN'};
    }
     $.ajax({type: "post",
        url: urlPrice,
        data: input,
        dataType: 'json',
        success: function(data){
            console.log(data)
            //update echart
            var echartLine = echarts.init(document.getElementById('MACD_chart'), theme);
            echartLine.setOption({
                title: {
                  text: getUrlParameter('ticker'),
                  subtext: 'Line Chart'
                },
                tooltip: {
                  trigger: 'axis'
                },
                legend: {
                  x: 220,
                  y: 40,
                  data: ['MACD','MACD_Signal','MACD_Hist']
                },
                toolbox: {
                  show: true,
                  feature: {
                    magicType: {
                      show: true,
                      title: {
                        line: 'Line',
                        bar: 'Bar',
                        stack: 'Stack',
                        tiled: 'Tiled'
                      },
                      type: ['line', 'bar', 'stack', 'tiled']
                    },
                    restore: {
                      show: true,
                      title: "Restore"
                    },
                    saveAsImage: {
                      show: true,
                      title: "Save Image"
                    }
                  }
                },
                calculable: true,
                xAxis: [{
                  type: 'category',
                  boundaryGap: false,
                  data: data.date
                }],
                yAxis: [{
                  type: 'value'
                }],
                series: [{
                  name: 'MACD',
                  type: 'line',
                  smooth: true,
                  data: data.MACD
                },{
                  name: 'MACD_Signal',
                  type: 'line',
                  smooth: true,
                  data: data.MACD_Signal
                },{
                  name: 'MACD_Hist',
                  type: 'bar',
                  smooth: true,
                  data: data.MACD_Hist
                }]
              });
            },
        fail: function(){
            console.log('query fail.');
          }
        });
}

//initial set click on
$("#subStockName").click(function(){
  var stockName = $('#stockName').val();
  //alert(stockName);
  window.location.href = 'stock?ticker='+stockName;
  window.event.returnValue=false;
});

function initial_kpi(){
  if($('#average_price').length){
    var urlPrice = "backend/get_average_price";
    var input = {'ticker': getUrlParameter('ticker')};
    console.log(input);
    if (input === undefined){
        var input = {'ticker': 'AMZN'};
    }
     $.ajax({type: "post",
        url: urlPrice,
        data: input,
        dataType: 'json',
        success: function(data){
            console.log(data)
            $('#average_price').html(data.data.toFixed(2));
            },
        fail: function(){
            console.log('query fail.');
          }
        });
  }
  
  if($('#highest_price').length){
    var urlPrice = "backend/get_highest_price";
    console.log(input);
    if (input === undefined){
        var input = {'ticker': 'AMZN'};
    }
     $.ajax({type: "post",
        url: urlPrice,
        data: input,
        dataType: 'json',
        success: function(data){
            console.log(data)
            $('#highest_price').html(data.data.toFixed(2));
            },
        fail: function(){
            console.log('query fail.');
          }
        });
  }  

  if($('#lowest_price').length){
    var urlPrice = "backend/get_lowest_price";
    console.log(input);
    if (input === undefined){
        var input = {'ticker': 'AMZN'};
    }
     $.ajax({type: "post",
        url: urlPrice,
        data: input,
        dataType: 'json',
        success: function(data){
            console.log(data)
            $('#lowest_price').html(data.data.toFixed(2));
            },
        fail: function(){
            console.log('query fail.');
          }
        });
  }  
    
}


//initial table and charts


$( document ).ready(function() {
	console.log( "ready!" );
  //update UserID
  if($('#userID').length){
    var input = {'user': 123};
    var urlGetUser = 'backend/get_userId';
    $.ajax({type: "post",
    url: urlGetUser,
    data: input,
    dataType: 'json',
    success: function(data){
        console.log(data)
        $('#userID').html(data.name);
        $('#signUp').html('Logout');
        $('#signUp').attr("href","logout");
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) { 
                    //alert("Status: " + textStatus + "Error: " + errorThrown); 
                }
              });
  }
  if($('#userName').length){
    var urlGetUser = 'backend/get_userId';
    $.ajax({type: "post",
    url: urlGetUser,
    data: input,
    dataType: 'json',
    success: function(data){
        console.log(data)
        $('#userName').html(data.name);
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) { 
                    //alert("Status: " + textStatus + "Error: " + errorThrown); 
                    $('#leftSideMenu').empty();
                }
              });
  }

  initial_kpi();
  if($('#stockNews').length){
    //updata News
    var url = "backend/get_news";
    var input = {'ticker': getUrlParameter('ticker')};
    console.log(input);
    $('#stockNewsID').html(getUrlParameter('ticker'));
    if (input === undefined){
        var input = {'ticker': "AMZN"};
    }
    $.ajax({type: "post",
        url: url,
        data: input,
        dataType: 'json',
        success: function(data){
            console.log(data)
            $.each(data.article, function(i, item) {
                $('#stockNews').append(
                    $('<li>').append(
                        $('<div>').attr('class','block').append(
                            $('<div>').attr('class','block_content').append(
                                $('<h2>').attr('class','title').append(
                                    $('<a>').append(item.title)
                                ),
                                $('<div>').attr('class','byline').append(item.date),
                                $('<p>').attr('class','excerpt').append(item.summary)
                            )
                        )
                    )
                );
            });
        },
    fail: function(){
            console.log('query fail.');
          }
        }); 
  }
  if($('#SMA_chart').length){
    update_sma();
  }

  if($('#RSI_chart').length){
    update_rsi();
  }

  if($('#MACD_chart').length){
    update_macd();
  }

  if($('#reservation').length){
    var urlRange = 'backend/get_yearRange';
    var input = {'ticker': getUrlParameter('ticker')};
    $.ajax({type: "post",
              url: urlRange,
              data: input,
              dataType: 'json',
              success: function(data){
                  console.log('in setting echarts line range');
                  //update echart
                  dateRange.from_time = data.min;
                  dateRange.to_time = data.maz;
                  $('#reservation').val(data.min+' - '+ data.max);
                  //alert($('#reservation').val());
                  $('#reservation').on('apply.daterangepicker', function(ev, picker) {
                    dateRange.from_time = picker.startDate.format('YYYY-MM-DD'); 
                    dateRange.to_time = picker.endDate.format('YYYY-MM-DD');
                    console.log(dateRange);
                    update_sma();
                    update_rsi();
                    update_macd();
                  });
                },
              error: function(XMLHttpRequest, textStatus, errorThrown) { 
                    alert("Status: " + textStatus + "Error: " + errorThrown); 
                }
              });
  }

  if($('#stockTableID').length){
    //get data
    var urlPrice = "backend/get_price";
    var input = {'ticker': getUrlParameter('ticker')};
    console.log(input);
    if (input === undefined){
        var input = {'ticker': 'AMZN'};
    }
    $.ajax({type: "post",
        url: urlPrice,
        data: input,
        dataType: 'json',
        success: function(data){
            console.log(data)
            //initial table
            var typeSet = data.typeName;
            $('#stockTableID').html(getUrlParameter('ticker'));
            //update table
            $.each(data.tableData.date, function(i,item){
              $('#priceTable').append(
                  $('<tr>').append(
                      $('<td>').append(data.tableData[data.typeName[0]][i]),
                      $('<td>').append(data.tableData[data.typeName[1]][i]),
                      $('<td>').append(data.tableData[data.typeName[2]][i]),
                      $('<td>').append(data.tableData[data.typeName[3]][i]),
                      $('<td>').append(data.tableData[data.typeName[4]][i]),
                      $('<td>').append(data.tableData[data.typeName[5]][i]),
                      $('<td>').append(data.tableData[data.typeName[6]][i])
                      ));
            });
            $('#stockTable').DataTable();
                },
        fail: function(){
            console.log('query fail.');
          }
        });
  }

  if($('#stocksTable').length){
    var urlPrice = "backend/get_stocks";
    var input = {'ticker': 'AMZN'};
    $.ajax({type: "post",
        url: urlPrice,
        data: input,
        dataType: 'json',
        success: function(data){
            console.log(data)
            //update table
            stocksData = data;
            $.each(data.data, function(i,item){
              $('#priceTable').append(
                  $('<tr>').append(
                    $('<td>').append(
                      $('<input>').attr({
                        type: "checkbox",
                        id: "check-all",
                        class: "flat",
                        onclick: "checkBoxClick()"
                      })),
                    $('<td>').append(data.data[i][data.colName[6]]),
                    $('<td>').append(data.data[i][data.colName[0]]),
                    $('<td>').append(data.data[i][data.colName[1]]),
                    $('<td>').append(data.data[i][data.colName[2]]),
                    $('<td>').append(data.data[i][data.colName[3]]),
                    $('<td>').append(data.data[i][data.colName[4]]),
                    $('<td>').append(data.data[i][data.colName[5]])
                    ));
            });
            $('#stocksTable').DataTable();
                },
        fail: function(){
            console.log('query fail.');
          }
        });
  }
});




var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};