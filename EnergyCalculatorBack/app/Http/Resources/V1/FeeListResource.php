<?php

namespace App\Http\Resources\V1;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class FeeListResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'description' => $this->description,
            'tusd' => 'R$ ' . number_format(floatval($this->tusd), 2, ',', '.'),
            'te_verde' => 'R$ ' . number_format(floatval($this->te_verde), 2, ',', '.'),
            'te_amarela' => 'R$ ' . number_format(floatval($this->te_amarela), 2, ',', '.'),
            'te_vermelha' => 'R$ ' . number_format(floatval($this->te_vermelha), 2, ',', '.'),
            'discount' => $this->discount,
            'city' => 
                [
                'name' => ucwords(strtolower($this->city->name)),
                'flag' => $this->city->flag,
                'company' => $this->city->company,
                'monthPeriod' => substr($this->city->validityperiod, 0, 2),
                'yearPeriod' => substr($this->city->validityperiod, -4),
                'state' => 
                    [
                    'uf' => $this->city->state->uf,
                    'name' => $this->city->state->name
                    ]
                ]
        ];
    }
}
