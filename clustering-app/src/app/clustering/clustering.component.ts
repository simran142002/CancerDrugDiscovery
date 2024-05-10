import { Component } from '@angular/core';
import { ClusteringService } from '../clustering.service';

@Component({
  selector: 'app-clustering',
  templateUrl: './clustering.component.html',
  styleUrl: './clustering.component.css'
})
export class ClusteringComponent {
  features = ['IC50', 'IC90', 'EC50', 'Einf', 'AUC'];
  nClusters = 3;
  clusters: number[]=[];
  accuracy: number | undefined;
  mse: number | undefined;
  drugCombinationResults: any[] = [];
  cancerType: string = '';
  predictionResult: any;
  targetVariable: string = "";
  sensitivityPredictionResult: any;
  method: string = "";
  drugs: string[] =[];
  results: any[] = [];
  attribute: string = "";
  visualizationData: any;
  constructor(private clusteringService: ClusteringService) { }

  clusterData(): void {
    const data = { features: this.features, n_clusters: this.nClusters };
    this.clusteringService.clusterData(data).subscribe(
      clusters => {
        this.clusters = clusters;
      },
      error => {
        console.error('Error clustering data:', error);
      }
    );
  }

  predictCancer(cancer_type: any) {
    if (!cancer_type) {
      alert('Please enter a cancer type.');
      return;
    }
    
    this.clusteringService.predictCancer(cancer_type).subscribe(
      (data) => {
        this.predictionResult = data;
      },
      (error) => {
        console.error('Error predicting cancer:', error);
      }
    );
  }

  predictSensitivity(targetVariable: any) {
    if (!targetVariable) {
      alert('Please enter a target variable.');
      return;
    }
    
    this.clusteringService.predictSensitivity(targetVariable).subscribe(
      (data) => {
        this.sensitivityPredictionResult = data;
      },
      (error) => {
        console.error('Error predicting sensitivity:', error);
      }
    );
  } 

  calculateCombinedResponse() {
    console.log(this.method, this.drugs.length);
    if (!this.method || !this.drugs) {
      alert('Please enter a method and two drugs.');
      return;
    }
    const requestData = { method: this.method, drugs: this.drugs };
    this.clusteringService.calculateCombinedResponse(requestData).subscribe(
      (data) => {
        this.results = data.results;
      },
      (error) => {
        console.error('Error calculating combined response:', error);
      }
    );
  }
  
  visualizeData(): void {
    // Validate input fields
    if (!this.cancerType || !this.attribute) {
      alert('Please enter both cancer type and attribute.');
      return;
    }
  
    // Prepare request data
    const requestData = {
      cancerType: this.cancerType,
      attribute: this.attribute
    };
    console.log(requestData);
  
    // Call the API service method to visualize data
    this.clusteringService.visualizeData(requestData).subscribe(
      (data) => {
        // Assign the base64-encoded image data to the visualizationData variable
        this.visualizationData = data.image_base64;
        console.log(this.visualizationData);
      },
      (error) => {
        console.error('Error visualizing data:', error);
        // Handle error if needed
      }
    );
  }
  
}
