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
    return this.http.post<any>(this.url + '/uploaddayahead', formData)
  }

  fetchRevisions(state: any, date: any) {
    return this.http.post<any>(this.url + '/fetchrevisions', {"state": state, "date": date})

  }

  fetchRevisionsData(state: any, date: any, revision: any) {
    return this.http.post<any>(this.url + '/fetchrevisionsdata', {"state": state, "date": date, "revision": revision})
  }

  fetchPendingEntry() {
    return this.http.get<any>(this.url + '/pendingentries')
  }

  downloadDayAheadReport(state: any, date: any, revision: any) {
    return this.http.post<any>(this.url + '/downloaddayahead', {"state": state, "date": date, "revision": revision}, {
      responseType: 'blob' as 'json'  // This is necessary to handle Blob data correctly
    })
  }



}
