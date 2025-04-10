import { Injectable } from '@angular/core';
import { api_url } from '../helpers/urlentry';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {

  url = api_url;

  constructor(private http: HttpClient) { }


  fetchDayUploadStatus() {
    return this.http.get<any>(this.url + '/uploadstatus')
  }


  mapeChart(formData: any) {
    return this.http.post<any>(this.url+'/mapechart', {"params":formData})
  }

  actualForecastComp(formData: any) {
    return this.http.post<any>(this.url+'/actualforecastcomp', {"params":formData})
  }

  fetchDayRangeStatus(formDate:any) {
    return this.http.post<any>(this.url + '/dayrangestatus', {"params":formDate}) 
  }

  fetchWeekRangeStatus(formDate:any) {
    return this.http.post<any>(this.url + '/weekrangestatus', {"params":formDate}) 
  }

  fetchMonthRangeStatus(formDate:any) {
    return this.http.post<any>(this.url + '/monthrangestatus', {"params":formDate}) 
  }

  fetchYearRangeStatus(formDate:any) {
    return this.http.post<any>(this.url + '/yearrangestatus', {"params":formDate}) 
  }



}
