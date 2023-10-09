import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { api_url } from '../helpers/urlentry';




@Injectable({
  providedIn: 'root'
})



export class DayAheadForecastService {

  url = api_url;

  constructor(private http: HttpClient) { }

  uploadDayAheadFile(formData: any) {
    return this.http.post<any>(this.url + '/upload', formData)
  }
}
