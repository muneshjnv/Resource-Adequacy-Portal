import { DatePipe } from '@angular/common';
import { Component, ElementRef, ViewChild } from '@angular/core';
import { UntypedFormBuilder, UntypedFormGroup, Validators } from '@angular/forms';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { ToastService } from 'src/app/account/login/toast-service';
import { DayAheadForecastService } from 'src/app/core/services/day-ahead-forecast.service';
import { TokenStorageService } from 'src/app/core/services/token-storage.service';
import Swal from 'sweetalert2';
import * as jspreadsheet from "jspreadsheet-ce";




const today = new Date();


@Component({
  selector: 'app-view-dayahead',
  templateUrl: './view-dayahead.component.html',
  styleUrls: ['./view-dayahead.component.scss']
})
export class ViewDayaheadComponent {

  userData: any;


  loading: boolean = false;

  // data: number[][] = new Array<Array<number>>();

  submit!: boolean;

  formsubmit!: boolean;

  data: any[][] = [];

  uploadTime: any = '-'
  uploadDate: any = '-'
  revision: any = '-'
  uploadedBy: any = '-'



  breadCrumbItems!: Array<{}>;
  validationform!: UntypedFormGroup;

  revisionsData: any[] = [];

  @ViewChild("spreadsheet", {static: true}) spreadsheet !: ElementRef<any>;

  constructor(private modalService: NgbModal, private formBuilder: UntypedFormBuilder,public toastService: ToastService, private TokenStorageService: TokenStorageService , private dayAheadForecast: DayAheadForecastService ,private datePipe: DatePipe) { }



  ngOnInit(): void {
    this.breadCrumbItems = [
      { label: 'Past Uploads' },
      { label: 'Day Ahead Forecast', active: true }
    ];

    this.userData = this.TokenStorageService.getUser();

    this.validationform = this.formBuilder.group({
      // firstName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      // lastName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      // userName: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      // city: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      state: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      // zip: ['', [Validators.required, Validators.pattern('[a-zA-Z0-9]+')]],
      fetchDate: [today],
      revisions: ['', [Validators.required]]
    });



    



    if(this.userData['role'] == 'user'){

      

      // console.log("Rinnegan")

      // console.log(this.state_id_dict[this.userData['username']]);
    
      this.validationform.get('state')!.setValue(this.userData['state_id']);
      this.validationform.get('state')!.disable();

      this.fetchDataBasedOnDate(this.validationform.get('state')!.value, this.validationform.get('fetchDate')!.value);
    }

    this.validationform.get('fetchDate')!.valueChanges.subscribe((date) => {
      if (date) {
        this.fetchDataBasedOnDate(this.validationform.get('state')!.value, date);
      }
      
    });

    this.validationform.get('state')!.valueChanges.subscribe((state) => {
      if (state) {
        // console.log(state);

        this.fetchDataBasedOnDate(state, this.validationform.get('fetchDate')!.value);
      }
      
    });






    // end of ngOnInit
  }

  fetchDataBasedOnDate(state: string, date: Date): void {
    // Replace with your API endpoint

    // Make an API call
    this.dayAheadForecast.fetchRevisions(state, date.toLocaleDateString('en-GB')).subscribe((data: any) => {
      // Update the dropdownData array with the response
      if(data["status"] == "success") {
        this.revisionsData = data['revisions'];
        this.validationform.get('revisions')!.enable();
      }
      else {
        this.validationform.get('revisions')!.reset("");
        this.validationform.get('revisions')!.disable();

        setTimeout(() => {
          Swal.fire({
            text: data['message'],
            icon: 'warning',
            confirmButtonColor: 'rgb(3, 142, 220)',
            confirmButtonText: 'OK'
          });
        }, 1500);
        

      }
      
    });
  }

    fetchData() {
      this.loading = true;
      if(this.validationform.valid) {
        // console.log("ngsubmit hit!")
        this.dayAheadForecast.fetchRevisionsData(this.validationform.get('state')!.value, this.validationform.get('fetchDate')!.value.toLocaleDateString('en-GB'), this.validationform.get('revisions')!.value).subscribe((data: any)=> {
          
          this.loading = false;
          if(data["status"] == "failure") {

            Swal.fire({
              text: data['message'],
              icon: 'warning',
              confirmButtonColor: 'rgb(3, 142, 220)',
              confirmButtonText: 'OK'
            });

            

          }

          else {
            if(data["status"] == "success") {
              // console.log(typeof data["data"])
              // console.log(data)
              this.spreadsheet.nativeElement.jexcel.setData(data["data"])
              this.uploadDate = data["date"]
              this.uploadTime = data["time"]
              this.revision = data["revision"]
              this.uploadedBy = data["role"]

            }
          }
          
        })


      }




      else {
        // console.log("Form is invalid!")
      }
      
      

    }

    validSubmit() {
      this.submit = true;
    }

    get form() {
      return this.validationform.controls;
    }

    formSubmit() {
      this.formsubmit = true;
    }

    ngAfterViewInit() {
      jspreadsheet(this.spreadsheet.nativeElement, {
      data: this.data,
      // freezeColumns: 2,
      footers: [[ ' ','Total MUs', '=ROUND(SUM(C1:C96),2)' , '=ROUND(SUM(D1:D96),2)' , '=ROUND(SUM(E1:E96),2)','=ROUND(SUM(F1:F96),2)' , '=ROUND(SUM(G1:G96),2)' , '=ROUND(SUM(H1:H96),2)','=ROUND(SUM(I1:I96),2)' , '=ROUND(SUM(J1:J96),2)' , '=ROUND(SUM(K1:K96),2)','=ROUND(SUM(L1:L96),2)' , '=ROUND(SUM(M1:M96),2)' , '=ROUND(SUM(N1:N96),2)','=ROUND(SUM(O1:O96),2)' , '=ROUND(SUM(P1:P96),2)' , '=ROUND(SUM(Q1:Q96),2)','=ROUND(SUM(R1:R96),2)' , '=ROUND(SUM(S1:S96),2)' , '=ROUND(SUM(T1:T96),2)', '=ROUND(SUM(U1:U96),2)' ]],
  
      tableOverflow: true,
      tableWidth: '1200px',
      tableHeight: '400px',
      columns: [
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
                colspan: 2, 
                
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
                colspan: 2,
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
              colspan: 2,
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
  
      if(colIndex == 2) {
        const exactValue = value.toString()
        // console.log(typeof value);
        if(typeof value !== 'number' && Number.isNaN(Number.parseInt(exactValue))){
          cell.style.background = '#ffcccb'
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

  

}

