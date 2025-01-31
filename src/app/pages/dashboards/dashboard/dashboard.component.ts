import { Component, OnInit } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { DashboardService } from 'src/app/core/services/dashboard.service';
import Swal from 'sweetalert2';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';
import { TokenStorageService } from 'src/app/core/services/token-storage.service';
import { ToastService } from 'src/app/core/services/toast-service';

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
  basicYearHeatmapChart: any;

  MarketplaceChart: any;
  MarketplaceChartAF: any;

  dataArrived: boolean = false;

  // bread crumb items
  breadCrumbItems!: Array<{}>;
  submit!: boolean;
  afSubmit! : boolean
  formsubmit!: boolean;

  loading: boolean = false;
  weekloading: boolean = false;
  monthloading: boolean = false;
  yearloading: boolean = false;
  mapeloading: boolean = false;
  afloading: boolean = false;


  public day_data:any = [];
  public week_data: any = [];
  public month_data: any = [];
  public year_data: any = [];

  selectedOption: string = 'day';

  mape_day_ahead: any = [];
  dates_list: any = []
  mape_week_ahead: any = []
  mape_month_ahead: any = []
  mape_data: any = []
  demand_data: any = []
  mape_title: any = "MAPE"
  fa_compare_title = "Comparison"
  userData: any;

  state_id_dict: any = {'bh_state': 1, 'jh_state':2, 'gr_state': 3, 'wb_state': 4, 'dvc_state':5, 'si_state': 7}

  dayForm!: UntypedFormGroup; // Define the form group
  weekForm!: UntypedFormGroup; // Define the form group
  monthForm!: UntypedFormGroup; // Define the form group
  yearForm!: UntypedFormGroup; // Define the form group


  validationform!: UntypedFormGroup;
  faform!: UntypedFormGroup;

  constructor(private dashboardService: DashboardService, private formBuilder: UntypedFormBuilder, private TokenStorageService: TokenStorageService, public toastService: ToastService) {
  }

  ngOnInit(): void {
    /**
     * BreadCrumb
     */

    this.userData = this.TokenStorageService.getUser();



    this.breadCrumbItems = [
      { label: 'Dashboards' },
      { label: 'Dashboard', active: true }
    ];

    this._marketplaceChart('["--vz-primary","--vz-success", "--vz-warning"]');


    this._actualForecastmarketplaceChart('["--vz-primary","--vz-success", "--vz-warning", "--vz-danger"]');


          // Initialize the form group
          this.dayForm = this.formBuilder.group({
            dayRange: [{"from": this.getPreviousMonthDates()["startDate"], "to":this.getPreviousMonthDates()["endDate"] }] // Initialize the control for the date range picker
          });
    
        this.weekForm = this.formBuilder.group({
        weekRange: [{"from": this.getPreviousMonthDates()["startDate"], "to":this.getPreviousMonthDates()["endDate"] }] // Initialize the control for the date range picker
        });
    
        this.monthForm = this.formBuilder.group({
            monthRange: [{"from": this.getPreviousMonthDates()["startDate"], "to":this.getPreviousMonthDates()["endDate"] }] // Initialize the control for the date range picker
            });
        

        this.yearForm = this.formBuilder.group({
            yearRange: [{"from": this.getPreviousMonthDates()["startDate"], "to":this.getPreviousMonthDates()["endDate"] }] // Initialize the control for the date range picker
            });

    this.dashboardService.fetchDayUploadStatus().subscribe((data: any) => {

        if (data && data["day"] && data["week"] && data["month"] && data["year"]) {

             //   console.log(data);
      this.day_data = data["day"];
      this.week_data = data["week"];
      this.month_data = data["month"];
      this.year_data = data["year"];

    // //   console.log(data);



      // Updating the form controls with the fetched dates
        this.dayForm.patchValue({
            dayRange: { from: new Date(data["day_dates"]["start_date"]), to: new Date(data["day_dates"]["end_date"]) }
        });



    this.weekForm.patchValue({
        weekRange: { from: new Date(data["week_dates"]["start_date"]), to: new Date(data["week_dates"]["end_date"]) }
    });

    this.monthForm.patchValue({
        monthRange: { from: new Date(data["month_dates"]["start_date"]), to: new Date(data["month_dates"]["end_date"]) }
    });

    this.yearForm.patchValue({
        yearRange: { from: new Date(data["year_dates"]["start_date"]), to: new Date(data["year_dates"]["end_date"]) }
    });
        this._basicHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
        this._basicWeekHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
        this._basicMonthHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
        this._basicYearHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');

        
        this.dataArrived = true;


        }
   

        // if(this.userData['state_id'] != 6){}

    //     })

    // this.dashboardService.fetchDayUploadStatus().subscribe({
    //     next: (data) => {
    //         // handle data
    //     },
    //     error: (error) => {
    //         console.error("Failed to fetch data:", error);
    //     }
    });


    this.validationform = this.formBuilder.group({
        // firstName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        // lastName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        // userName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        // city: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        state: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        // zip: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        monthDate: [{"from": this.getPreviousMonthDates()["startDate"], "to":this.getPreviousMonthDates()["endDate"] }],
      });


      

      this.faform = this.formBuilder.group({
        // firstName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        // lastName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        // userName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        // city: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        state: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        // zip: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
        monthDate: [{"from": this.getPreviousMonthDates()["startDate"], "to":this.getPreviousMonthDates()["endDate"] }],
      });



      if(this.userData['role'] == 'user'){

        // console.log("Rinnegan")
  
        // console.log(this.state_id_dict[this.userData['username']]);
      
        this.validationform.get('state')!.setValue(this.userData['state_id']);
        this.validationform.get('state')!.disable();


        this.faform.get('state')!.setValue(this.userData['state_id']);
        this.faform.get('state')!.disable();
      }

      else {
        this.validationform.get('state')!.setValue(this.userData['state_id']);
      }
    

      this.dashboardMapeComp();




    

    

   
  }



  weekAhead() {
    // console.log("week ahead clicked!")
  }

  monthAhead() {
    // console.log("Month ahead clicked!")
  }

  yearAhead() {
    // console.log("Year ahead clicked!")
  }

  validSubmit() {
    this.submit = true;
  }

  afValidSubmit() {
    this.afSubmit = true;
  }

  formSubmit() {
    this.formsubmit = true;
  }
  get form() {
    return this.validationform.controls;
  }

  get afform(){
    return this.faform.controls;
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

private _basicYearHeatmapChart(colors: any) {
    colors = this.getChartColorsArray(colors);
    this.basicYearHeatmapChart = {
        series: this.year_data,
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


    fetchForDay() {

        
        const formData = {
            // state: this.validationform.get('state')!.value,
            fromDate: this.dayForm.get('dayRange')?.value["from"].toLocaleDateString('en-GB'),
            toDate: this.dayForm.get('dayRange')?.value["to"].toLocaleDateString('en-GB')
          };

          this.loading = true


          this.dashboardService.fetchDayRangeStatus(formData).subscribe((data: any) => {
            this.loading = false;

            //   console.log(data);
            //   console.log("API Hit and Response receieved")
              this.day_data = data["day"];
            //   this.week_data = data["week"];
            //   this.month_data = data["month"];
              this._basicHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
            //   this._basicWeekHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
            //   this._basicMonthHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
              
              this.dataArrived = true;
        
            })


            
    }

    fetchForWeek() {

        const formData = {
            // state: this.validationform.get('state')!.value,
            fromDate: this.weekForm.get('weekRange')?.value["from"].toLocaleDateString('en-GB'),
            toDate: this.weekForm.get('weekRange')?.value["to"].toLocaleDateString('en-GB')
          };

          this.weekloading = true;
          

          this.dashboardService.fetchWeekRangeStatus(formData).subscribe((data: any) => {
                this.weekloading = false;
            //   console.log(data);
            //   console.log("API Hit and Response receieved")
            //   this.day_data = data["day"];
              this.week_data = data["week"];
            //   this.month_data = data["month"];
            //   this._basicHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
              this._basicWeekHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
            //   this._basicMonthHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
              
              this.dataArrived = true;
        
            })

    }

    fetchForMonth() {

        this.monthloading = true;

        const formData = {
            // state: this.validationform.get('state')!.value,
            fromDate: this.monthForm.get('monthRange')?.value["from"].toLocaleDateString('en-GB'),
            toDate: this.monthForm.get('monthRange')?.value["to"].toLocaleDateString('en-GB')
          };

          this.dashboardService.fetchMonthRangeStatus(formData).subscribe((data: any) => {
                this.monthloading = false;
            //   console.log(data);
            //   console.log("API Hit and Response receieved")
            //   this.day_data = data["day"];
            //   this.week_data = data["week"];
              this.month_data = data["month"];
            //   this._basicHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
            //   this._basicWeekHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
              this._basicMonthHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
              
              this.dataArrived = true;
        
            })

    }


    dashboardMapeComp() {
        const formData = {
            state: this.validationform.get('state')!.value,
            fromDate: this.validationform.get('monthDate')?.value["from"].toLocaleDateString('en-GB'),
            toDate: this.validationform.get('monthDate')?.value["to"].toLocaleDateString('en-GB')
          };

        this.dashboardService.mapeChart(formData).subscribe((res: any) => {
            this.mapeloading = false;
            if(res["status"] == "failure") {
                this.MarketplaceChart.series = [];
                this.mape_title = res["title"];
            }

            else {
                // console.log("Data Received!") 
                // console.log(res);

                this.MarketplaceChart.series = res["data"];
                this.mape_title = res["title"];
                // console.log(this.MarketplaceChart.series);
                // console.log(this.MarketplaceChart.title)


                this.MarketplaceChartAF.series = res["comp_data"]["data"]
                this.fa_compare_title = res["comp_data"]["title"];


            }
        })
    }

    


    confirm() {
        
        
            // console.log()
            if(this.validationform.valid) {
                // const formData = new FormData();
                this.mapeloading = true;
                const formData = {
                    state: this.validationform.get('state')!.value,
                    fromDate: this.validationform.get('monthDate')?.value["from"].toLocaleDateString('en-GB'),
                    toDate: this.validationform.get('monthDate')?.value["to"].toLocaleDateString('en-GB')
                  };

                this.dashboardService.mapeChart(formData).subscribe((res: any) => {
                    this.mapeloading = false;
                    if(res["status"] == "failure") {
                        this.MarketplaceChart.series = [];
                        this.mape_title = res["title"];
                    }

                    else {
                        // console.log("Data Received!") 
                        // console.log(res);

                        this.MarketplaceChart.series = res["data"];
                        this.mape_title = res["title"];
                        // console.log(this.MarketplaceChart.series);
                        // console.log(this.MarketplaceChart.title)


                        this.MarketplaceChartAF.series = res["comp_data"]["data"]
                        this.fa_compare_title = res["comp_data"]["title"];
 

                    }
                })
             }
        
    }

    afConfirm() {
        
        
        // console.log()
        if(this.faform.valid) {
            // const formData = new FormData();
            this.afloading = true;
            const formData = {
                state: this.faform.get('state')!.value,
                fromDate: this.faform.get('monthDate')?.value["from"].toLocaleDateString('en-GB'),
                toDate: this.faform.get('monthDate')?.value["to"].toLocaleDateString('en-GB')
              };

            this.dashboardService.actualForecastComp(formData).subscribe((res: any) => {
                this.afloading = false;
                if(res["status"] == "failure") {
                    this.MarketplaceChartAF.series = [];
                    this.fa_compare_title = res["title"];
                }

                else {
                    // console.log("Data Received!") 
                    // console.log(res);

                    this.MarketplaceChartAF.series = res["data"];
                    this.fa_compare_title = res["title"];
                    // console.log(this.MarketplaceChart.series);
                    // console.log(this.MarketplaceChart.title)

                    if("message" in res) {
                        this.toastService.show(res["message"], { classname: 'bg-success text-white', delay: 3000 });

                    }


                }
            })
         }
    
}


    fetchForYear() {

        this.yearloading = true;

        const formData = {
            // state: this.validationform.get('state')!.value,
            fromDate: this.yearForm.get('yearRange')?.value["from"].toLocaleDateString('en-GB'),
            toDate: this.yearForm.get('yearRange')?.value["to"].toLocaleDateString('en-GB')
          };

          this.dashboardService.fetchYearRangeStatus(formData).subscribe((data: any) => {
                this.yearloading = false;
            //   console.log(data);
            //   console.log("API Hit and Response receieved")
            //   this.day_data = data["day"];
            //   this.week_data = data["week"];
              this.year_data = data["year"];
            //   this._basicHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
            //   this._basicWeekHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
              this._basicYearHeatmapChart('["--vz-success", "--vz-danger", "--vz-warning"]');
              
              this.dataArrived = true;
        
            })

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



    private _actualForecastmarketplaceChart(colors: any) {
        colors = this.getChartColorsArray(colors);
        
        this.MarketplaceChartAF = {
            series: this.demand_data,  // Ensure timestamps are in UTC in your demand_data
            xaxis: {
                type: 'datetime',
                labels: {
                    formatter: function (val: string) {
                        if (!val) return "";  // Return an empty string if `val` is undefined
                        const date = new Date(val);
                        return date.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
                    },
                    style: {
                        colors: '#333',
                        fontSize: '12px'
                    }
                },
                tooltip: {
                    enabled: true,
                    formatter: function (val: string) {
                        if (!val) return "";  // Return an empty string if `val` is undefined
                    const date = new Date(val);
                    return date.toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' });
                    }
                }
            },
            yaxis: {
                labels: {
                    show: true,
                    formatter: function (y: number) {
                        if(y == 0){
                            return "No Data";
                        }
                        return y + " MW";  // Adjust label to display MW
                    },
                    style: {
                        colors: '#333',
                        fontSize: '12px'
                    }
                },

            },
            
            chart: {
                height: 350,
                type: 'line',
                zoom: {
                    enabled: true
                },
                toolbar: {
                    show: true
                }
            },


            
            stroke: {
                curve: 'smooth',
                width: 3, 
            },
            colors: colors,
        };
    }
    




    // Utility function to format dates to 'YYYY-MM-DD'




    formatDateToYYYYMMDD(date: Date): string {
    return date.toISOString().split('T')[0];
  }


  
}
