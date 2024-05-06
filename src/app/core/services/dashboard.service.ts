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




}
