<?php

namespace App\Http\Resources\V1;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class CityResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => ucwords(strtolower($this->name)),
            'flag' => $this->flag,
            'company' => $this->company,
            'monthPeriod' => substr($this->validityperiod, 0, 2),
            'yearPeriod' => substr($this->validityperiod, -4),
            'state' => [
                'uf' => $this->state->uf,
                'name' => $this->state->name
                ]
        ];
    }
}
