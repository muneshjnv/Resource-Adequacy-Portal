import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { DashboardService } from 'src/app/core/services/dashboard.service';
import Swal from 'sweetalert2';

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

  MarketplaceChart: any;

  dataArrived: boolean = false;

  // bread crumb items
  breadCrumbItems!: Array<{}>;
  submit!: boolean;
  formsubmit!: boolean;


  public day_data:any = [];
  public week_data: any = [];
  public month_data: any = [];

  selectedOption: string = 'day';

  mape_day_ahead: any = [];
  dates_list: any = []
  mape_week_ahead: any = []
  mape_month_ahead: any = []
  mape_data: any = []
  mape_title: any = "MAPE"


  validationform!: UntypedFormGroup;

  constructor(private dashboardService: DashboardService, private formBuilder: UntypedFormBuilder) {
  }

  ngOnInit(): void {
    /**
     * BreadCrumb
     */
    this.breadCrumbItems = [
      { label: 'Dashboards' },
      { label: 'Dashboard', active: true }
    ];

    this._marketplaceChart('["--vz-primary","--vz-success", "--vz-warning"]');

    this.dashboardService.fetchDayUploadStatus().subscribe((data: any) => {
      console.log(data);
      this.day_data = data["day"];
      this.week_data = data["week"];
      this.month_data = data["month"];
      this._basicHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
      this._basicWeekHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
      this._basicMonthHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
      
      this.dataArrived = true;

    })


    this.validationform = this.formBuilder.group({
        // firstName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        // lastName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        // userName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        // city: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        state: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        // zip: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        monthDate: [{"from": this.getPreviousMonthDates()["startDate"], "to":this.getPreviousMonthDates()["endDate"] }],
      });




    

    

   
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

  validSubmit() {
    this.submit = true;
  }

  formSubmit() {
    this.formsubmit = true;
  }
  get form() {
    return this.validationform.controls;
  }

  areStartingAndEndingDatesOfSameMonth(fromDate:Date, toDate: Date) {
    // Calculate the first day (starting date) of the same month as toDate
    const firstDayOfMonth = new Date(toDate.getFullYear(), toDate.getMonth(), 1);
  
    // Calculate the last day (ending date) of the same month as fromDate
    const lastDayOfMonth = new Date(fromDate.getFullYear(), fromDate.getMonth() + 1, 0);
  
    return fromDate.getTime() === firstDayOfMonth.getTime() && toDate.getTime() === lastDayOfMonth.getTime();
  }
    
  
  daysInMonth(date: Date): number {
    const year = date.getFullYear();
    const month = date.getMonth() + 1; // Months in JavaScript are 0-indexed
  
    // Use Date.UTC to avoid time zone issues
    const lastDayOfMonth = new Date(Date.UTC(year, month, 0));
    return lastDayOfMonth.getUTCDate();
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
                        from: 0,
                        to: 0,
                        name: 'Late Upload',
                        color: colors[2]
                    },
                    {
                        from: 2,
                        to: 2,
                        name: 'Not Uploaded',
                        color: colors[1]
                    },
                    {
                        from: 1,
                        to: 1,
                        name: 'Uploaded',
                        color: colors[0]
                    },
                    ]
                }
            }
        },
        tooltip: {
            
            custom: function(opts: any) {
                // if (w && w.config && w.config.series && w.config.series[seriesIndex] && w.config.series[seriesIndex].data && w.config.series[seriesIndex].data[dataPointIndex]) {
                    const uploadTime =  opts.ctx.w.config.series[opts.seriesIndex].data[opts.dataPointIndex].upload_time;
                    // const uploadTime = w.config.series[seriesIndex].data[dataPointIndex].upload_time;
                    if (uploadTime) {
                        return '<b>Upload Time: </b> ' + uploadTime ;
                            
                            
                    }
                   
    
                    
                // }

                else {
                    return "<b>Not Uploaded</b>" 
                }
                
                   
            }
        }

    
    };


}


private _basicWeekHeatmapChart(colors: any) {
    colors = this.getChartColorsArray(colors);
    this.basicWeekHeatmapChart = {
        series: this.week_data,
        chart: {
            height: 300,
            width: '90%',
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
                        from: 0,
                        to: 0,
                        name: 'Late Upload',
                        color: colors[2]
                    },
                    {
                        from: 2,
                        to: 2,
                        name: 'Not Uploaded',
                        color: colors[1]
                    },
                    {
                        from: 1,
                        to: 1,
                        name: 'Uploaded',
                        color: colors[0]
                    },
                    ]
                }
            }
        },
        tooltip: {
            
            custom: function(opts: any) {
                // if (w && w.config && w.config.series && w.config.series[seriesIndex] && w.config.series[seriesIndex].data && w.config.series[seriesIndex].data[dataPointIndex]) {
                    const uploadTime =  opts.ctx.w.config.series[opts.seriesIndex].data[opts.dataPointIndex].upload_time;
                    // const uploadTime = w.config.series[seriesIndex].data[dataPointIndex].upload_time;
                    if (uploadTime) {
                        return '<b>Upload Time: </b> ' + uploadTime ;
                            
                            
                    }
                   
    
                    
                // }

                else {
                    return "<b>Not Uploaded</b>" ;
                }
                
                    
            }
        }
    };
}




private _basicMonthHeatmapChart(colors: any) {
    colors = this.getChartColorsArray(colors);
    this.basicMonthHeatmapChart = {
        series: this.month_data,
        xaxis: {
            type: 'datetime'
          },  
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
                        from: 0,
                        to: 0,
                        name: 'Late Upload',
                        color: colors[2]
                    },
                    {
                        from: 2,
                        to: 2,
                        name: 'Not Uploaded',
                        color: colors[1]
                    },
                    {
                        from: 1,
                        to: 1,
                        name: 'Uploaded',
                        color: colors[0]
                    },
                    ]
                }
            }
        },
        tooltip: {
            
            custom: function(opts: any) {
                // if (w && w.config && w.config.series && w.config.series[seriesIndex] && w.config.series[seriesIndex].data && w.config.series[seriesIndex].data[dataPointIndex]) {
                    const uploadTime =  opts.ctx.w.config.series[opts.seriesIndex].data[opts.dataPointIndex].upload_time;
                    // const uploadTime = w.config.series[seriesIndex].data[dataPointIndex].upload_time;
                    if (uploadTime) {
                        return '<b>Upload Time: </b> ' + uploadTime ;
                            
                            
                    }
                   
    
                    
                // }

                else {
                    return "<b>Not Uploaded</b>" ;
                }
                
                    
            }
        }
    };
}

getPreviousMonthDates() {
    // Get the current date
    const currentDate = new Date();

    // Calculate the previous month's starting date
    const previousMonthStartDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1);

    // Calculate the previous month's ending date
    const previousMonthEndDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 0);

    // Format the dates as strings (in "YYYY-MM-DD" format)
    const previousMonthStartDateString = previousMonthStartDate.toISOString().split('T')[0];
    const previousMonthEndDateString = previousMonthEndDate.toISOString().split('T')[0];

    return {
        startDate: previousMonthStartDate,
        endDate: previousMonthEndDate
    };
}


    confirm() {
        if ( !(this.areStartingAndEndingDatesOfSameMonth(this.validationform.get('monthDate')!.value["from"], this.validationform.get('monthDate')!.value["to"]))) {
            Swal.fire({text:'Please choose a Proper month (Starting and ending date)!',confirmButtonColor: 'rgb(3, 142, 220)',});
          }
        else {
            // console.log()
            if(this.validationform.valid) {
                // const formData = new FormData();
                const formData = {
                    state: this.validationform.get('state')!.value,
                    fromDate: this.validationform.get('monthDate')?.value["from"].toLocaleDateString('en-GB'),
                    toDate: this.validationform.get('monthDate')?.value["to"].toLocaleDateString('en-GB')
                  };

                this.dashboardService.mapeChart(formData).subscribe((res: any) => {
                    if(res["status"] == "failure") {
                        this.MarketplaceChart.series = [];
                        this.mape_title = res["title"];
                    }

                    else {
                        console.log("Data Received!") 

                        this.MarketplaceChart.series = res["data"];
                        this.mape_title = res["title"];
                        console.log(this.MarketplaceChart.series);
                        console.log(this.MarketplaceChart.title)
 

                    }
                })
             }
        }
    }



    private _marketplaceChart(colors: any) {
        colors = this.getChartColorsArray(colors);
        this.MarketplaceChart = {
            series:this.mape_data,
            xaxis: {
                type: 'datetime'
              },  
              yaxis: {
                labels: {
                    show: true,
                    formatter: function (y: number) {
                        return y + "%";
                    },
                    style: {
                        colors: '#333', // Adjust y-axis label color as needed
                        fontSize: '12px' // Adjust the label font size
                    }
                }
            },
            chart: {
                height: 350,
                type: 'line',
                zoom: {
                    enabled: false
                },
                toolbar: {
                    show: true
                }
            },
            // title: {
            //     text: this.mape_title,
            //     align: 'center',
            //     margin: 10,
            //     offsetX: 0,
            //     offsetY: 0,
            //     floating: false,
            //     style: {
            //       fontSize:  '14px',
            //       fontWeight:  'bold',
            //       fontFamily:  undefined,
            //       color:  '#263238'
            //     },
            // },
            dataLabels: {
                enabled: false
            },
           
            stroke: {
                curve: 'smooth',
                width: 3
            },
           
            
            colors: colors,
            
        };
    }






  
}
