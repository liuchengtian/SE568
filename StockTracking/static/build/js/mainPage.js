$( document ).ready(function() {
	console.log( "ready!" );

    //updata News
	var url = "backend/get_news";
	var input = {ticker: "AMZN"};
    console.log(input);
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

    //initial price
    var date = [];
    var dataOpen = [];
    var dataHigh = [];
    var dataLow = [];
    var dataClose = [];

    //get data
    var urlPrice = "backend/get_price";
    $.ajax({type: "post",
        url: urlPrice,
        data: input,
        dataType: 'json',
        success: function(data){
            console.log(data)
            var date = data.date;
            var dataOpen = data.open;
            var dataClose = data.close;
            var dataHigh = data.high;
            var dataLow = data.low;
            //update echart
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
            var echartLine = echarts.init(document.getElementById('echart_line'), theme);
            echartLine.setOption({
                title: {
                  text: 'AMZN',
                  subtext: 'Subtitle'
                },
                tooltip: {
                  trigger: 'axis'
                },
                legend: {
                  x: 220,
                  y: 40,
                  data: ['Open', 'Close', 'High','Low']
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
                  data: date
                }],
                yAxis: [{
                  type: 'value'
                }],
                series: [{
                  name: 'Open',
                  type: 'line',
                  smooth: true,
                  itemStyle: {
                    normal: {
                    }
                  },
                  data: dataOpen
                }, {
                  name: 'Close',
                  type: 'line',
                  smooth: true,
                  itemStyle: {
                    normal: {
                    }
                  },
                  data: dataClose
                }, {
                  name: 'High',
                  type: 'line',
                  smooth: true,
                  itemStyle: {
                    normal: {
                    }
                  },
                  data: dataHigh
                },  {
                  name: 'Low',
                  type: 'line',
                  smooth: true,
                  itemStyle: {
                    normal: {
                    }
                  },
                  data: dataLow
                }]
            });

            //update table
            $.each(data.date, function(i,item){
                $('#priceTable').append(
                    $('<tr>').append(
                        $('<th>').attr('scope','row').append(i),
                        $('<td>').append(item),
                        $('<td>').append(dataOpen[i]),
                        $('<td>').append(dataHigh[i]),
                        $('<td>').append(dataLow[i]),
                        $('<td>').append(dataClose[i]),
                        $('<td>').append('0'),
                        $('<td>').append('0')
                        ));
            });
                },
        fail: function(){
            console.log('query fail.');
          }
        });
});



// $('#content ul').append(
    // $('<li>').append(
        // $('<a>').attr('href','/user/messages').append(
            // $('<span>').attr('class', 'tab').append("Message center")
// )))