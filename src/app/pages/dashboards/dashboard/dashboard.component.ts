import { Component, OnInit } from '@angular/core';
import { DashboardService } from 'src/app/core/services/dashboard.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})

/**
 * Ecommerce Component
 */
export class DashboardComponent implements OnInit {

  basicHeatmapChart: any;
  basicWeekHeatmapChart: any;
  basicMonthHeatmapChart: any;

  dataArrived: boolean = false;

  // bread crumb items
  breadCrumbItems!: Array<{}>;


  public day_data:any = [];
  public week_data: any = [];
  public month_data: any = [];

  selectedOption: string = 'day';

  constructor(private dashboardService: DashboardService) {
  }

  ngOnInit(): void {
    /**
     * BreadCrumb
     */
    this.breadCrumbItems = [
      { label: 'Dashboards' },
      { label: 'Dashboard', active: true }
    ];

    this.dashboardService.fetchDayUploadStatus().subscribe((data: any) => {
      console.log(data);
      this.day_data = data["day"];
      this.week_data = data["week"];
      this.month_data = data["month"];
      this._basicHeatmapChart('["--vz-success", "--vz-danger"]');
      this._basicWeekHeatmapChart('["--vz-success", "--vz-danger"]');
      this._basicMonthHeatmapChart('["--vz-success", "--vz-danger"]');
      this.dataArrived = true;

    })


    

    

   
  }



  weekAhead() {
    console.log("week ahead clicked!")
  }

  monthAhead() {
    console.log("Month ahead clicked!")
  }

  yearAhead() {
    console.log("Year ahead clicked!")
  }

  

  private getChartColorsArray(colors: any) {
    colors = JSON.parse(colors);
    return colors.map(function (value: any) {
        var newValue = value.replace(" ", "");
        if (newValue.indexOf(",") === -1) {
            var color = getComputedStyle(document.documentElement).getPropertyValue(newValue);
            if (color) {
                color = color.replace(" ", "");
                return color;
            }
            else return newValue;;
        } else {
            var val = value.split(',');
            if (val.length == 2) {
                var rgbaColor = getComputedStyle(document.documentElement).getPropertyValue(val[0]);
                rgbaColor = "rgba(" + rgbaColor + "," + val[1] + ")";
                return rgbaColor;
            } else {
                return newValue;
            }
        }
    });
}




  // generateStatusData() {
  //   return this.http
  // }


  private _basicHeatmapChart(colors: any) {
    colors = this.getChartColorsArray(colors);
    this.basicHeatmapChart = {
        series: this.day_data,
        chart: {
            height: 300,
            width: '100%',    
            type: 'heatmap',
            offsetX: 0,
            offsetY: -8,
            toolbar: {
                show: false
            }
        },
        dataLabels: {
            enabled: false
        },
        legend: {
            show: true,
            horizontalAlign: 'center',
            offsetX: 0,
            offsetY: 20,
            markers: {
                width: 20,
                height: 6,
                radius: 2,
            },
            itemMargin: {
                horizontal: 12,
                vertical: 0
            },
        },
        colors: colors,
        plotOptions: {
            heatmap: {
                colorScale: {
                    ranges: [{
                        from: 1,
                        to: Number.MAX_VALUE,
                        name: 'Uploaded',
                        color: colors[0]
                    },
                    {
                        from: 0,
                        to: 0,
                        name: 'Not Uploaded',
                        color: colors[1]
                    },
                    ]
                }
            }
        },
        // tooltip: {
        //     y: [{
        //         formatter: function (y: any) {
        //             if (typeof y !== "undefined") {
        //                 return y.toFixed(0) + "k";
        //             }
        //             return y;
        //         }
        //     }]
        // },
    };


}


private _basicWeekHeatmapChart(colors: any) {
    colors = this.getChartColorsArray(colors);
    this.basicWeekHeatmapChart = {
        series: this.week_data,
        chart: {
            height: 300,
            width: '100%',
            type: 'heatmap',
            offsetX: 0,
            offsetY: -8,
            toolbar: {
                show: false
            }
        },
        dataLabels: {
            enabled: false
        },
        legend: {
            show: true,
            horizontalAlign: 'center',
            offsetX: 0,
            offsetY: 20,
            markers: {
                width: 20,
                height: 6,
                radius: 2,
            },
            itemMargin: {
                horizontal: 12,
                vertical: 0
            },
        },
        colors: colors,
        
        plotOptions: {
            heatmap: {
                
                colorScale: {
                    ranges: [{
                        from: 1,
                        to: Number.MAX_VALUE,
                        name: 'Uploaded',
                        color: colors[0]
                    },
                    {
                        from: 0,
                        to: 0,
                        name: 'Not Uploaded',
                        color: colors[1]
                    },
                    ]
                }
            }
        },
        // tooltip: {
        //     y: [{
        //         formatter: function (y: any) {
        //             if (typeof y !== "undefined") {
        //                 return y.toFixed(0) + "k";
        //             }
        //             return y;
        //         }
        //     }]
        // },
    };
}




private _basicMonthHeatmapChart(colors: any) {
    colors = this.getChartColorsArray(colors);
    this.basicMonthHeatmapChart = {
        series: this.month_data,
        chart: {
            height: 300,
            width: '100%',
            type: 'heatmap',
            offsetX: 0,
            offsetY: -8,
            toolbar: {
                show: false
            }
        },
        dataLabels: {
            enabled: false
        },
        legend: {
            show: true,
            horizontalAlign: 'center',
            offsetX: 0,
            offsetY: 20,
            markers: {
                width: 20,
                height: 6,
                radius: 2,
            },
            itemMargin: {
                horizontal: 12,
                vertical: 0
            },
        },
        colors: colors,
        
        plotOptions: {
            heatmap: {
                
                colorScale: {
                    ranges: [{
                        from: 1,
                        to: Number.MAX_VALUE,
                        name: 'Uploaded',
                        color: colors[0]
                    },
                    {
                        from: 0,
                        to: 0,
                        name: 'Not Uploaded',
                        color: colors[1]
                    },
                    ]
                }
            }
        },
        // tooltip: {
        //     y: [{
        //         formatter: function (y: any) {
        //             if (typeof y !== "undefined") {
        //                 return y.toFixed(0) + "k";
        //             }
        //             return y;
        //         }
        //     }]
        // },
    };
}






  
}
