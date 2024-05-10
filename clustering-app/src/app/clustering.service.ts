import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ClusteringService {

  private baseUrl = 'http://localhost:5000';
  private baseUrl1 = 'http://localhost:5001'; // Base URL for the first API
  private baseUrl2 = 'http://localhost:5002'; // Base URL for the second API
  private apiUrl = 'http://localhost:5003/calculate_combined_response';

  constructor(private http: HttpClient) { }
  
  clusterData(data: any): Observable<number[]> {
    return this.http.post<number[]>(`${this.baseUrl}/cluster`, data);
  }
  
  predictCancer(cancerType: string): Observable<any> {
    return this.http.post<any>(`${this.baseUrl2}/predict_cancer`, { cancer_type: cancerType });
  }

  predictSensitivity(target: string): Observable<any> {
    return this.http.post<any>(`${this.baseUrl1}/predict`, { target });
  }

  analyzeDrugCombinations(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/analyze`);
  }

  calculateCombinedResponse(data: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, data);
  }

  visualizeData(requestData: any): Observable<any> {
    return this.http.post<any>(`http://localhost:5004/visualize`, requestData);
  }
  
}
