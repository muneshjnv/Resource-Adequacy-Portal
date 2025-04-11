import { Component, ElementRef, TemplateRef, ViewChild } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastService } from '../../timingentry/timingentry-pending/toast-service';
import { DayAheadForecastService } from 'src/app/core/services/day-ahead-forecast.service';
import { DatePipe } from '@angular/common';
import { TokenStorageService } from 'src/app/core/services/token-storage.service';
import Swal from 'sweetalert2';
import * as jspreadsheet from 'jspreadsheet-ce';
import * as XLSX from 'xlsx';
import { WeekAheadForecastService } from 'src/app/core/services/week-ahead-forecast.service';


// const today = new Date();


@Component({
  selector: 'app-weekahead',
  templateUrl: './weekahead.component.html',
  styleUrls: ['./weekahead.component.scss']
})
export class WeekaheadComponent {



  

  
  excelData: { header: any[]; rows: any[] } | null = null;

  // bread crumb items
  breadCrumbItems!: Array<{}>;

  spreadsheetData: any = [[]];

  loadedData: boolean = false;
  
  // disabledDate: Date = new Date(today.getTime() + 24 * 60 * 60 * 1000);
 
// Subtract one day from current time                       
  // this.disabledDate.setDate(this.disabledDate.getDate() - 1);
  

  tooltipvalidationform!: UntypedFormGroup;

  formsubmit!: boolean;

  uploading: boolean = false;

  

  // calendar
  // calendarEvents!: any[];
  // editEvent: any;
  // formEditData!: UntypedFormGroup;
  validationform!: UntypedFormGroup;

  // newEventDate: any;
  // category!: any[];
  submitted = false;
  submit!: boolean;
  previewClicked: boolean = false;
  userData: any;


  state_id_dict: any = {'bh_state': 1, 'jh_state':2, 'gr_state': 3, 'wb_state': 4, 'dvc_state':5, 'si_state': 7}

  data: any;

  // Calendar click Event
  // formData!: UntypedFormGroup;
  @ViewChild('editmodalShow') editmodalShow!: TemplateRef<any>;
  @ViewChild('modalShow') modalShow !: TemplateRef<any>;
  @ViewChild("spreadsheet", {static: true}) spreadsheet !: ElementRef<any>;
  // worksheets: jspreadsheet.worksheetInstance[];

  constructor(private modalService: NgbModal, private formBuilder: UntypedFormBuilder,public toastService: ToastService, private TokenStorageService: TokenStorageService  ,private datePipe: DatePipe, private weekAheadForecastService: WeekAheadForecastService) { }
  
  ngOnInit(): void {

    this.breadCrumbItems = [
      { label: 'File Uploads' },
      { label: 'Week Ahead Forecast', active: true }
    ];
    /**
     * BreadCrumb
     */
    this.userData = this.TokenStorageService.getUser();


    


   

    
    
    // });

    this.validationform = this.formBuilder.group({
      // firstName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      // lastName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      // userName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      // city: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      state: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      // zip: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      disabledDate: [{"from": this.getNextMonday(), "to":new Date(this.getNextMonday().getTime() + 6*24 * 60 * 60 * 1000) }],
      excelFile: [null]
    });


    if(this.userData['role'] == 'user'){

      // console.log("Rinnegan")

      // console.log(this.state_id_dict[this.userData['username']]);
    
      this.validationform.get('state')!.setValue(this.userData['state_id']);
      this.validationform.get('state')!.disable();
      this.validationform.get('disabledDate')!.disable()
    }

    this.weekAheadForecastService.fetchFormat().subscribe((res: any) => {
      if(res["status"] == "success") {
        this.data = res["data"];
        this.spreadsheet.nativeElement.jexcel.setData(this.data);

        Swal.fire({text:'Data is prefilled with zeros, Please upload the file preview the data and then Upload!',confirmButtonColor: 'rgb(3, 142, 220)',});


      }
      else {
        Swal.fire({text:'There is a problem, Please contact ERLDC IT!',confirmButtonColor: 'rgb(3, 142, 220)',});

      }
      
    })
    





  }

  


  // Validation


  // this._fetchData();



  tempData: any = [];
  
  
  validSubmit() {
    this.submit = true;
  }
  
  /**
   * Returns form
   */
   get form() {
    return this.validationform.controls;
  }
  
  
  ngAfterViewInit() {
      jspreadsheet(this.spreadsheet.nativeElement, {
      data: this.data,
      // freezeColumns: 2,
      footers: [[ ' ', ' ','Total MUs', '=ROUND(SUM(D1:D672)/4000,2)' , '=ROUND(SUM(E1:E672)/4000,2)' , '=ROUND(SUM(F1:F672)/4000,2)','=ROUND(SUM(G1:G672)/4000,2)' , '=ROUND(SUM(H1:H672)/4000,2)' , '=ROUND(SUM(I1:I672)/4000,2)','=ROUND(SUM(J1:J672)/4000,2)' , '=ROUND(SUM(K1:K672)/4000,2)' , '=ROUND(SUM(L1:L672)/4000,2)','=ROUND(SUM(M1:M672)/4000,2)' , '=ROUND(SUM(N1:N672)/4000,2)' , '=ROUND(SUM(O1:O672)/4000,2)','=ROUND(SUM(P1:P672)/4000,2)' , '=ROUND(SUM(Q1:Q672)/4000,2)' , '=ROUND(SUM(R1:R672)/4000,2)','=ROUND(SUM(S1:S672)/4000,2)' , '=ROUND(SUM(T1:T672)/4000,2)' , '=ROUND(SUM(T1:T672)/4000,2)', '=ROUND(SUM(U1:U672)/4000,2)' ]],
  
      tableOverflow: true,
      tableWidth: '1200px',
      tableHeight: '400px',
      columns: [
        {
          type: 'calendar',
          title: 'Date',
          width: '120'
        },
        {
            type: 'numeric',
            title: 'Block',
            width: '50',
            readOnly: true
            
        },
        {
            type: 'text',
            title: 'Period',
            width: '150',
            readOnly: true
            
        },
        {
            type: 'numeric',
            title: 'MW',
            width:'150',
            decimal: '.',
            mask: '0.00'
        },
        {
          type: 'numeric',
          title: 'MW',
          width:'100',
          decimal: '.',
            mask: '0.00'
      },
      {
        type: 'numeric',
        title: 'MW',
        width:'100',
        decimal: '.',
        mask: '0.00'
    },
      {
        type: 'numeric',
        title: 'MW',
        width:'100',
        decimal: '.',
        mask: '0.00'
      },
      {
        type: 'numeric',
        title: 'MW',
        width:'100',
        decimal: '.',
        mask: '0.00'
      },
    {
      type: 'numeric',
      title: 'MW',
      width:'100',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'180',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'100',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'225'
    },{
      type: 'numeric',
      title: 'MW',
      width:'225',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'225',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'100',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'300',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'175',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'175',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'300',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'300',
      decimal: '.',
      mask: '0.00'
    },{
      type: 'numeric',
      title: 'MW',
      width:'300',
      decimal: '.',
      mask: '0.00'
    },
    {
      type: 'numeric',
      title: 'MVar',
      width:'300',
      decimal: '.',
      mask: '0.00'
      
    },
    ],
    nestedHeaders:[
      
        [
            {
                title: 'Time',
                colspan: 3, 
                
            },
            {
              title: 'Forecasted Generation/ Availability',
              colspan: 12, 
              
              
          },
          {
            title: 'Gap between Demand & Availability (G) = (A)-(F)  Surplus(-) / Deficit (+)',
            colspan: 1, 
            
            
        },
        {
          title: 'Proposed Procurement',
          colspan: 2, 
          
        },
        {
          title: 'Shortages after day ahead procurement from market (J) =(G)-(H+I)  Surplus(-) / Deficit (+)',
          colspan: 1, 
          
      },
      {
        title: 'Relief through planned restrictions/ rostering/ power cuts (K)',
        colspan: 1, 
        
      },
      {
        title: 'Additional Load shedding proposed (L) = (J)-(K) Surplus(-) / Deficit (+)',
        colspan: 1, 
        
      },
      {
        title: 'Reactive Power Forecast',
        colspan: 1, 
        
      },
  
        ],
        [
            {
                title: '',
                colspan: 3,
            },
            {
              title: 'Forecasted Demand (A)',
              colspan: 1,
          },
          
  
            {
              title: 'From its own sources (Excluding Renewable)',
              colspan: 4, 
              
          },
          {
            title: 'From Renewable Sources',
            colspan: 4, 
            
        },
        {
          title: 'From ISGS & Other LTA & MTOA',
          colspan: 1, 
          
        },
        {
          title: 'From Bilateral Transaction (Advance + FCFS)',
          colspan: 1, 
          
        },
        {
          title: 'Total Availability',
          colspan: 1, 
          
        }, 
        {
          title: '',
          colspan: 1, 
          
        },  
        {
          title: 'Under Bilateral Transaction (Day Ahead+ Contingency) (H)',
          colspan: 1, 
          
        },
        {
          title: 'Through Power Exchange (I)',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },   {
          title: '',
          colspan: 1, 
          
        },   {
          title: '',
          colspan: 1, 
          
        },  
        {
          title: '',
          colspan: 1, 
          
        },  
        ],
        [
          {
              title: '',
              colspan: 3,
          },
          {
            title: '',
            colspan: 1,
        },
        
          {
            title: 'Thermal (Coal + Lignite)',
            colspan: 1, 
            
        },
        {
          title: 'Gas',
          colspan: 1, 
          
      },
        {
          title: 'Hydro',
          colspan: 1, 
          
      },
        {
          title: 'Total (B)',
          colspan: 1, 
          
      },
        {
        title: 'Solar',
        colspan: 1, 
        
        },
        {
          title: 'Wind',
          colspan: 1, 
          
        },
        {
          title: 'Other RES (biomass etc.)',
          colspan: 1, 
          
        },
        {
          title: 'Total (C)',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },  
        {
          title: '',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },
        {
          title: '',
          colspan: 1, 
          
        },   {
          title: '',
          colspan: 1, 
          
        },   {
          title: '',
          colspan: 1, 
          
        },    
  
        {
          title: '',
          colspan: 1, 
          
        },  
          
      ],
    ],
  
    updateTable(instance, cell, colIndex, rowIndex, value, displayedValue, cellName) {
  
      if(colIndex == 3) {
        const exactValue = value.toString()
        // console.log(typeof value);
        if(typeof value !== 'number' && Number.isNaN(Number.parseInt(exactValue))){
          cell.style.background = '#ffcccb'
          Swal.fire({text:'Your Data has some errors, They are highlighted. Please check and Update',confirmButtonColor: 'rgb(3, 142, 220)',});
        }
  
        const modifiedValue = value.toString()
      // console.log(modifiedValue)
      if(typeof modifiedValue === "number" || !Number.isNaN(Number.parseFloat(modifiedValue))) {
        // console.log("enter the dragon!")
        cell.style.background = 'white';
      }
      
      
        
        
      }
    },
  
   
  
    // onchange(element, cell, colIndex, rowIndex, newValue, oldValue) {
    //   // console.log('Rinnegan')
    //   // console.log(oldValue)
    //   // console.log(typeof newValue);
  
    //   // if(typeof newValue === 'number' ){
    //   //   cell.style.background = 'white';
    //   // }
  
    //   // console.log(Number.is(newValue));
    //   // const stringValue = cellValue.toString();
    //   const modifiedValue = newValue.toString()
    //   console.log(modifiedValue)
    //   console.log(typeof modifiedValue === "number" || !Number.isNaN(Number.parseFloat(modifiedValue)));
    //   if(typeof modifiedValue === "number" || !Number.isNaN(Number.parseFloat(modifiedValue))) {
    //     cell.style.background = 'blue';
    //   }
  
    // },
  
    
    
    
    
  
    
  
    
    
    });


        
  }
  
  formSubmit() {
    this.formsubmit = true;
  }
  
  
  confirm() {

  

    if(this.validationform.get('excelFile')!.value == null) {
      Swal.fire({text:'It seems you have not uploaded the file, Please upload the file!',confirmButtonColor: 'rgb(3, 142, 220)',});
  
    }
    else if ((this.validationform.get('disabledDate')?.value["to"]-this.validationform.get('disabledDate')?.value["from"])/(24 * 60 * 60 * 1000) != 6 || this.validationform.get('disabledDate')?.value["from"].getDay() != 1) {
      Swal.fire({text:'Please choose a week starting from Monday to Sunday!',confirmButtonColor: 'rgb(3, 142, 220)',});
    }
    else {

      

      // console.log("Entered Else part!")

      if(this.validationform.valid) {

        Swal.fire({
          title: 'Are you sure?',
          text: 'You won\'t be able to revert this!',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonColor: 'rgb(3, 142, 220)',
          cancelButtonColor: 'rgb(243, 78, 78)',
          confirmButtonText: 'Yes, Insert it!'
        }).then(result => {
          if (result.value) {
            const formData = new FormData();
            formData.append('state', this.validationform.get('state')!.value);
            formData.append('fromDate', this.validationform.get('disabledDate')?.value["from"].toLocaleDateString('en-GB'));
            formData.append('toDate', this.validationform.get('disabledDate')?.value["to"].toLocaleDateString('en-GB'));
            formData.append('excelFile', this.validationform.get('excelFile')!.value);
            formData.append('data', JSON.stringify(this.spreadsheet.nativeElement.jexcel.getData()))

            this.uploading = true;
              
              this.weekAheadForecastService.uploadWeekAheadFile(formData).subscribe((res: any)=> {

                this.uploading = false;

                if('error' in res) {
                  // console.log(res['error'])
                }
                else {
                  // console.log(res["message"]);
                  // this.toastService.show(res['message'], { classname: 'bg-success text-white', delay: 5000 });
        
                  
                  Swal.fire({
                    text: res['message'],
                    icon: 'success',
                    confirmButtonColor: 'rgb(3, 142, 220)',
                    confirmButtonText: 'OK'
                  });

                  this.spreadsheet.nativeElement.jexcel.setData(this.data);
        
        
        
        
                }
          
              })
                  }
        });
    
    
    
    
      }

    }
   
    
  }
  
  
  onUpload() {
    // console.log(this.validationform.get('excelFile')!.value)
    if(this.validationform.get('excelFile')!.value == null) {
      Swal.fire({text:'It seems you have not uploaded the file, Please upload the file!',confirmButtonColor: 'rgb(3, 142, 220)',});
  
    }
    if(this.validationform.valid) {
  
      // console.log(this.validationform.get('disabledDate')!.value);
  
      const formData = new FormData();
    formData.append('state', this.validationform.get('state')!.value);
    formData.append('fromDate', this.validationform.get('disabledDate')!.value["from"]);
    formData.append('toDate', this.validationform.get('disabledDate')!.value["to"]);
    formData.append('excelFile', this.validationform.get('excelFile')!.value);
    formData.append('data', JSON.stringify(this.spreadsheet.nativeElement.jexcel.getData()))
      
      this.weekAheadForecastService.uploadWeekAheadFile(formData).subscribe((res: any)=> {
        if('error' in res) {
          // console.log(res['error'])
        }
        else {
          // console.log(res["message"]);
          // this.toastService.show(res['message'], { classname: 'bg-success text-white', delay: 5000 });

          
          Swal.fire({
            text: res['message'],
            icon: 'success',
            confirmButtonColor: 'rgb(3, 142, 220)',
            confirmButtonText: 'OK'
          });




        }
  
      })
  
    }
  
  
  
    
  }
  
  
  get formData() {
    return this.tooltipvalidationform.controls;
  }
  
  
  previewButtonClicked() {
    this.previewClicked = true;
  }
  
  downloadExcel() {
    // Define the path to the Excel file in the assets folder
    const excelFilePath = 'assets/Week-Ahead Demand Forecast format (from States).xlsx';
  
    // Trigger the download by creating a temporary <a> element
    const a = document.createElement('a');
    a.href = excelFilePath;
    a.download = 'sample.xlsx'; // Specify the desired file name
  
    // Programmatically trigger a click event to initiate the download
    a.click();
  }
  
  
  handleFileInput(event: any) {

    // console.log(this.spreadsheet.nativeElement.jexcel);
    const file = event.target.files[0];
    this.validationform.get('excelFile')!.setValue(file);
    if (!file) return;
  
    const reader = new FileReader();
    reader.onload = (e: any) => {
      const binaryString = e.target.result;
      const workbook = XLSX.read(binaryString, { type: 'binary' });
      // console.log(workbook.SheetNames);
      // console.log("sheetnames above")
      const firstSheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[firstSheetName];
  
      // Convert worksheet data to a nested header structure
      this.excelData = this.convertSheetData(worksheet);
      // console.log(this.excelData);

      let flag: boolean = false;

      console.log(this.data);
      console.log("before this is data!")

      const secondColumnValues: any[] = this.data.map((row:any) => row[2]);

      secondColumnValues.push('23:45 - 24:00')


      this.tempData = [];
      for(var i =0; i < this.excelData.rows.length; i++) {
        if((this.excelData.rows[i][1] >= 1 && this.excelData.rows[i][1] <= 96) && secondColumnValues.includes(this.excelData.rows[i][2]) ){
          
          this.tempData.push(this.excelData.rows[i].slice(0,22))

        }

        // this.excelData.rows[i][0] = new Date((this.excelData.rows[i][0] - 25569) * 86400 * 1000);
        
        
      }

      for(var i=0; i <  this.tempData.length; i++) {
        this.tempData[i][0] = new Date((this.tempData[i][0] - 25569) * 86400 * 1000).toLocaleDateString('en-GB');
      }

      // console.log(this.tempData)

      let totalCount = this.getTotalElements(this.tempData);

      this.loadedData = true;

      // console.log(this.tempData[0])
      // console.log(this.tempData[0].length)


      if (this.tempData.length!==96*7|| totalCount !== 96*22*7){
        Swal.fire({text:'The data you have uploaded is not in the proper format, Please upload based on the format provided above.',confirmButtonColor: 'rgb(3, 142, 220)',}).then(() => {
          this.validationform.get('excelFile')!.setValue(null); // Reset form control
          event.target.value = null; // Clear file input
        }); 
        return;
      }

      let allZeroes = true;
      for (let i = 0; i < this.tempData.length; i++) {
        if (Number(this.tempData[i][3]) !== 0) { // Index 1 for second column
          allZeroes = false;
          break;
        }
      }

      if (allZeroes) {
        Swal.fire({
          text: 'Forecasted Demand contains all zeroes. Please correct the data.',
          confirmButtonColor: 'rgb(3, 142, 220)',
        }).then(() => {
         this.validationform.get('excelFile')!.setValue(null); // Reset form control
         event.target.value = null; // Clear file input
       });
        return;
      }

      Swal.fire({text:'Data is successfully loaded, you can now preview the data!',confirmButtonColor: 'rgb(3, 142, 220)',});

 


    //   if (this.tempData.length!==0){
    //    // Check if column 2 (index 1) contains all zeroes
    //    let allZeroes = true;
    //    for (let i = 0; i < this.tempData.length; i++) {
    //      if (Number(this.tempData[i][3]) !== 0) { // Index 1 for second column
    //        allZeroes = false;
    //        break;
    //      }
    //    }

    //    if (allZeroes) {
    //      Swal.fire({
    //        text: 'Forecasted Demand contains all zeroes. Please correct the data.',
    //        confirmButtonColor: 'rgb(3, 142, 220)',
    //      }).then(() => {
    //       this.validationform.get('excelFile')!.setValue(null); // Reset form control
    //       event.target.value = null; // Clear file input
    //     });
    //      return;
    //    }

      
    //   if(totalCount == 96*22*7) {
    //       Swal.fire({text:'Data is successfully loaded, you can now preview the data!',confirmButtonColor: 'rgb(3, 142, 220)',});

    //   }
    // }
    //   else {
    //     // console.log(totalCount)
    //     // console.log(96*22*7);
    //     Swal.fire({text:'The data you have uploaded is not in the proper format, Please upload based on the format provided above.',confirmButtonColor: 'rgb(3, 142, 220)',}).then(() => {
    //       this.validationform.get('excelFile')!.setValue(null); // Reset form control
    //       event.target.value = null; // Clear file input
    //     });   

    //   }

      this.spreadsheet.nativeElement.jexcel.setData(this.tempData);

      



      
      

      // if(this.tempData.length >= 0 && (this.tempData.length != 96 || this.tempData[0].length !=  21)) {
      //   Swal.fire({text:'The data you have uploaded is not in the proper format, Please upload based on the format provided above.',confirmButtonColor: 'rgb(3, 142, 220)',});   

        
      // }
      // else {
      //   console.log("Entered to save the data!")
      //   // this.data = this.tempData;
      //   this.spreadsheet.nativeElement.jexcel.setData(this.data);
      //   Swal.fire({text:'Data is successfully loaded, you can now preview the data!',confirmButtonColor: 'rgb(3, 142, 220)',});


      // }
      
  
      // console.log(this.data);
      // this.ngAfterViewInit();
  
      // const x = this.spreadsheet.nativeElement;
      // console.log(x);
      // x.innerHTML = '';
  
  
      
  
      // this.ngAfterViewInit();
  
      // Swal.fire({text:'Data is successfully loaded, you can now preview the data!',confirmButtonColor: 'rgb(3, 142, 220)',});

      
  
  
  
      // this.previewClicked = true;
      
      
      
      
    };
    reader.readAsBinaryString(file);
  }

  getTotalElements(arr: any[][]): number {
    let totalCount = 0;
  
    for (const row of arr) {
      totalCount += row.length;
    }
  
    return totalCount;
  }
  
  convertSheetData(worksheet: XLSX.WorkSheet): { header: any[]; rows: any[] } {
    const data: any[] = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
    console.log(data);
    const headerRow = data[0];
    const headerMap = new Map<number, any>();
    
    console.log(headerRow);
    console.log("After printing!")

    // Map headers to their respective columns
    headerRow.forEach((header: any, index: any) => {
      if (!headerMap.has(index)) {
        headerMap.set(index, []);
      }
      headerMap.get(index).push(header);
    });
  
    const header: any[] = Array.from(headerMap.values()).map((headers: any[]) => {
      return headers.length > 1
        ? { text: headers[0], colspan: headers.length }
        : { text: headers[0], colspan: 1 };
    });
  
    const rows = data.slice(1);
  
    return { header, rows };
  }


  getNextMonday() {
    const today = new Date();
    const currentDayOfWeek = today.getDay();
    const daysUntilNextMonday = currentDayOfWeek === 1 ? 7 : (8 - currentDayOfWeek) % 7; // If today is Monday, go to next Monday
    const nextMonday = new Date(today);
    nextMonday.setDate(today.getDate() + daysUntilNextMonday); // Add the calculated days to the current date
    return nextMonday;
}

  
  
  
  
  
  


  


}
