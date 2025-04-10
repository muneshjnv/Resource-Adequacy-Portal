import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { api_url } from '../helpers/urlentry';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ReportsService {

  url = api_url+'/reports';

  constructor(private http: HttpClient) { }

  
  lineFlowReport (formDate:any) {
    return this.http.post<any>(this.url + '/lineflows', {"params":formDate}) 
  }

    // Function to download the file as a Blob
    downloadLineFlowsReport(downloadLink: any): Observable<Blob> {
      return this.http.post(this.url + '/downloadlineflows', { "downloadLink": downloadLink}, { responseType: 'blob' });
    }


    FetchDescription() {
      return this.http.get<any>(this.url + '/fetchmdpdescription') 
    }


    fetchDescriptionBasedData(formData: any) {
    
      return this.http.post<any>(this.url + '/mdpdescriptiondata', {"params":formData}) 

    }


}
